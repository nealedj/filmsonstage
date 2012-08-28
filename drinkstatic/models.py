from django.conf import settings
from django.template.defaultfilters import slugify
from drinkstatic import node_types

__author__ = 'davneale'

class Node(object):
    _url_slug = None
    _title_text = None
    _datestamp = None
    _template_path = None
    _thumbnail = None

    def __init__(self, dict):
        for k,v in dict.items():
            field_name = '_%s' % k
            if hasattr(self, field_name):
                setattr(self, field_name, v)

    @property
    def href(self):
        return '%s/%s' % (settings.BLOG_URL, self.slug)

    @property
    def title(self):
        return self._title_text

    @property
    def slug(self):
        return self._url_slug or slugify(self._title_text)

    @property
    def datestamp(self):
        return self._datestamp

    @property
    def template_path(self):
        return self._template_path

    @property
    def thumbnail(self):
        return self._thumbnail

class NodeList(object):
    def __init__(self, nodes_dict):
        self.nodes_dict = nodes_dict

    def get_by_slug(self, slug):
        return self.nodes_dict.get(slug)

    @property
    def list(self):
        return self.nodes_dict.values()

    @property
    def by_date_asc(self):
        return self.sort(lambda n: n.datestamp)

    @property
    def by_date_desc(self):
        return self.sort(lambda n: n.datestamp, reverse=True)

    def sort(self, fn, reverse=False):
        return sorted(self.nodes_dict.values(), key=fn, reverse=reverse)
