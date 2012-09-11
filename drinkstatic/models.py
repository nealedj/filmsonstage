from django.conf import settings
from django.template.defaultfilters import slugify
from google.appengine.ext import ndb

__author__ = 'davneale'

class Node(ndb.Model):
    FIELDS = ["url_slug", "title", "datestamp", "thumbnail", "snippet"]

    slug = ndb.StringProperty()
    v_url_slug = ndb.StringProperty()
    v_title = ndb.StringProperty()
    v_datestamp = ndb.DateTimeProperty()
    v_thumbnail = ndb.StringProperty()
    v_snippet = ndb.TextProperty()

    def __init__(self, *args, **kwargs):
        dict = kwargs.pop('dict', None)

        super(Node, self).__init__(*args, **kwargs)

        if dict:
            # this initialiser should only be called for creation from dictionary
            self.update_from_dict(dict)

    def update_from_dict(self, dict):
        for k,v in dict.items():
            field_name = k
            if field_name in self.FIELDS and hasattr(self, field_name):
                setattr(self, field_name, v)

    def to_dict(self):
        dict = {}
        for field in self.FIELDS:
            dict[field] = getattr(self, 'v_%s' % field)
        return dict

    @property
    def href(self):
        return '%s/%s' % (settings.BLOG_URL, self.slug)

    def get_url_slug(self):return self.v_url_slug
    def set_url_slug(self, url_slug):
        if url_slug:
            self.slug = self.v_url_slug = url_slug
    url_slug = property(get_url_slug, set_url_slug)

    def get_title(self): return self.v_title
    def set_title(self, title):
        self.v_title = title
        if not self.v_url_slug:
            self.slug = slugify(title)
    title = property(get_title, set_title)

    def get_datestamp(self):return self.v_datestamp
    def set_datestamp(self, datestamp):self.v_datestamp = datestamp
    datestamp = property(get_datestamp, set_datestamp)

    def get_thumbnail(self):return self.v_thumbnail
    def set_thumbnail(self, thumbnail):self.v_thumbnail = thumbnail
    thumbnail = property(get_thumbnail, set_thumbnail)

    def get_snippet(self):return self.v_snippet
    def set_snippet(self, snippet):self.v_snippet = snippet
    snippet = property(get_snippet, set_snippet)

    @classmethod
    def get_by_slug(cls, slug):
        return cls.query(cls.slug == slug).get()

class NodeList(object):
    sorted_list_limit = settings.NODE_LIST_LIMIT

    def __init__(self, node_list):
        self.nodes_dict = {}
        for node in node_list:
            self.nodes_dict[node.slug] = node

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
        return sorted(self.nodes_dict.values(), key=fn, reverse=reverse)[:self.sorted_list_limit]

class Template(ndb.Model):
    slug = ndb.StringProperty()
    source = ndb.TextProperty()
    datestamp = ndb.DateTimeProperty()

    @classmethod
    def get_by_template_key(cls, key):
        return cls.query(cls.slug == key).get()