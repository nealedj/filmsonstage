from django.conf import settings
from django.template.defaultfilters import slugify
from google.appengine.ext import ndb

__author__ = 'davneale'

class Node(ndb.Model):
    FIELDS = ["url_slug", "title", "datestamp", "thumbnail", "snippet", "archived"]

    slug = ndb.StringProperty()
    v_url_slug = ndb.StringProperty()
    v_title = ndb.StringProperty()
    v_datestamp = ndb.DateTimeProperty()
    v_thumbnail = ndb.StringProperty()
    v_snippet = ndb.TextProperty()
    v_archived = ndb.BooleanProperty(default=False)

    def __init__(self, *args, **kwargs):
        d = kwargs.pop('dict', None)

        super(Node, self).__init__(*args, **kwargs)

        if d:
            # this initialiser should only be called for creation from dictionary
            self.update_from_dict(d)

    def __new__(cls, *args, **kwargs):
        for field in cls.FIELDS:
            if not hasattr(cls, "get_%s" % field) or not hasattr(cls, "set_%s" % field):
                cls.add_property(field)

        return super(Node, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def add_property(cls, field):
        field_var = "v_%s" % field
        get_func = lambda self: getattr(self, field_var)
        set_func = lambda self, val: setattr(self, field_var, val)

        setattr(cls, field, property(get_func, set_func))



    def update_from_dict(self, d):
        for k,v in d.items():
            field_name = k
            if field_name in self.FIELDS and hasattr(self, field_name):
                setattr(self, field_name, v)

    def to_dict(self):
        d = {}
        for field in self.FIELDS:
            d[field] = getattr(self, 'v_%s' % field)
        return d

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

class NodeGroup(ndb.Model):
    class NodeGroupType:
        choices = ['live','archived','all_nodes']

    for choice in NodeGroupType.choices:
        setattr(NodeGroupType, choice, choice)

    date_key = ndb.DateProperty()
    count = ndb.IntegerProperty(default=0)
    nodes = ndb.StructuredProperty(Node, repeated=True)
    group_type = ndb.StringProperty(choices=NodeGroupType.choices)

    @classmethod
    def get_by_date_key(cls, date_key, group_type):
        return cls.query(cls.date_key == date_key, cls.group_type == group_type).get()
