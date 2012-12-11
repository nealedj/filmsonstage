import os
import glob
from django.template.context import Context
import logging
from google.appengine.ext import ndb
from drinkstatic.models import Node
from drinkstatic.templatetags.drinkstatic_tags import DrinkStaticNode
from drinkstatic.models import Template as DrinkStaticTemplate, NodeGroup

__author__ = 'davneale'

from django.conf import settings
from django.template import Template

class BasicGenerator(object):
    """
    Gets templates from directories defined in settings.DRINKSTATIC_TEMPLATE_DIRS
    """

    def __init__(self):
        self.template_dirs = getattr(settings, "DRINKSTATIC_TEMPLATE_DIRS")
        if not self.template_dirs:
            raise Exception('settings.DRINKSTATIC_TEMPLATE_DIRS was not defined or was emtpy')


    def save_templates_to_datastore(self, templates):
        futures = []
        for slug, raw in templates.items():
            template_obj = DrinkStaticTemplate.get_by_template_key(slug)
            if not template_obj:
                template_obj = DrinkStaticTemplate(slug=slug)
            template_obj.populate(
                source=raw
            )
            futures.append(template_obj.put_async())

        return futures

    def save_nodes_to_datastore(self, nodes):
        futures = []
        for slug, node in nodes.items():
            persist_node = Node.get_by_slug(node.slug)
            if not persist_node:
                node_obj = node
            else:
                node_obj = persist_node
                node_obj.update_from_dict(node.to_dict())

            futures.append(node_obj.put_async())

        return futures

    def group_nodes(self, nodes, group_type):
        futures = []
        groups = {}

        grouping_expr = lambda n: n.datestamp.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        for node in nodes.values():
            key = grouping_expr(node)

            if not key in groups:
                groups[key] = group = NodeGroup(date_key=key, group_type=group_type)
            else:
                group = groups[key]

            group.nodes.append(node)
            group.count += 1

        for key, group in groups.items():
            persist_group = NodeGroup.get_by_date_key(key, group_type)
            if not persist_group:
                group_obj = group
            else:
                group_obj = persist_group
                group_obj.populate(nodes=group.nodes, count=group.count)

            futures.append(group_obj.put_async())

        return futures

    def generate_all_nodes(self):
        nodes, templates, groups_live, groups_archived, groups_all = {}, {}, {}, {}, {}
        for dir in self.template_dirs:
            for filepath in glob.glob(os.path.join(dir, '*.html')):
                file = open(filepath)
                try:
                    raw = file.read().decode(settings.FILE_CHARSET)
                    name = os.path.split(filepath)[1]
                    node_obj = Node(dict=self.process_template(raw, filepath, name))
                    nodes[node_obj.slug], groups_all[node_obj.slug] = node_obj, node_obj
                    templates[node_obj.slug] = raw
                    (groups_archived if node_obj.archived else groups_live)[node_obj.slug] = node_obj
                except Exception as e:
                    logging.error('could not render template %s: %s' % (filepath, e))
                    raise
                finally:
                    file.close()


        futures = self.save_templates_to_datastore(templates) + self.save_nodes_to_datastore(nodes) + \
                  self.group_nodes(groups_all, NodeGroup.NodeGroupType.all_nodes) + \
                  self.group_nodes(groups_live, NodeGroup.NodeGroupType.live) + \
                  self.group_nodes(groups_archived, NodeGroup.NodeGroupType.archived)


        ndb.Future.wait_all(futures)

    def process_template(self, raw_template, origin, name):
        template = Template(raw_template, origin, name)

        return self._get_drinkstatic_data_from_nodes(template.nodelist, Context())

    def _get_drinkstatic_data_from_nodes(self, nodelist, context):
        bits = {}
        for node in nodelist:
            if hasattr(node, 'nodelist'):
                bits.update(self._get_drinkstatic_data_from_nodes(node.nodelist, context))
            elif isinstance(node, DrinkStaticNode):
                if node.node_type not in bits or not node.is_unique_on_page():
                    #ignore subsequent unique nodes
                    bits[node.node_type] = node.get_value(context)
            else:
                pass
        return bits