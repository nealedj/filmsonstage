import os
import glob
from django.template.context import Context
import logging
from drinkstatic.models import Node, NodeList
from drinkstatic.templatetags.drinkstatic_tags import DrinkStaticNode

__author__ = 'davneale'

from django.conf import settings
from django.template import Template

def get_all_nodes():
    template_dirs = settings.DRINKSTATIC_TEMPLATE_DIRS

    nodes = {}
    for dir in template_dirs:
        for filepath in glob.glob(os.path.join(dir, '*.html')):
            file = open(filepath)
            try:
                raw = file.read().decode(settings.FILE_CHARSET)
                name = os.path.split(filepath)[1]
                node_obj = Node(process_template(raw, filepath, name))
                nodes[node_obj.slug] = node_obj
            except Exception as e:
                logging.error('could not render template %s: %s' % (filepath, e))
            finally:
                file.close()

    return NodeList(nodes)

def process_template(raw_template, origin, name):
    template = Template(raw_template, origin, name)

    data = _get_drinkstatic_data_from_nodes(template.nodelist, Context())
    data['template_path'] = origin

    return data

def _get_drinkstatic_data_from_nodes(nodelist, context):
    bits = {}
    for node in nodelist:
        if hasattr(node, 'nodelist'):
            bits.update(_get_drinkstatic_data_from_nodes(node.nodelist, context))
        elif isinstance(node, DrinkStaticNode):
            if node.node_type not in bits or not node.is_unique_on_page():
                #ignore subsequent unique nodes
                bits[node.node_type] = node.get_value(context)
        else:
            pass
    return bits