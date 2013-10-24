import os
import glob
from PIL import Image
from django.template.context import Context
import logging
from google.appengine.ext import ndb
from drinkstatic.models import Node
from drinkstatic.templatetags.drinkstatic_tags import DrinkStaticNode
from drinkstatic.models import Template as DrinkStaticTemplate
from google.appengine.api import files

__author__ = 'davneale'

from django.conf import settings
from django.template import Template

from google.appengine.api.urlfetch import fetch

class BasicGenerator(object):
    """
    Gets templates from directories defined in settings.DRINKSTATIC_TEMPLATE_DIRS
    """

    def __init__(self, request):
        self.request = request
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

    def generate_all_nodes(self):
        nodes = {}
        templates = {}
        for dir in self.template_dirs:
            for filepath in glob.glob(os.path.join(dir, '*.html')):
                file = open(filepath)
                try:
                    raw = file.read().decode(settings.FILE_CHARSET)
                    name = os.path.split(filepath)[1]
                    node_obj = Node(dict=self.process_template(raw, filepath, name))
                    nodes[node_obj.slug] = node_obj
                    templates[node_obj.slug] = raw
                except Exception as e:
                    logging.error('could not render template %s: %s' % (filepath, e))
                    raise
                finally:
                    file.close()

        for node in nodes.values():
            thumbnail_path = self.save_thumbnail_jpg(node.thumbnail)
            node.thumbnail = thumbnail_path

        futures = self.save_templates_to_datastore(templates) + self.save_nodes_to_datastore(nodes)

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

    def save_thumbnail_jpg(self, thumbnail_path):
        url = self.request.build_absolute_uri(thumbnail_path)
        img_response = fetch(url)
        img = img_response.content

        out_file = files.blobstore.create(mime_type='application/octet-stream')

        img.thumbnail(settings.THUMBNAIL_WIDTH, Image.ANTIALIAS)

        img.save(out_file, "JPEG")

        files.finalize(out_file)

        return files.blobstore.get_blob_key(out_file)
