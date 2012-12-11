from google.appengine.api import memcache
from drinkstatic.models import Node, NodeList, NodeGroup
from django.conf import settings

__author__ = 'davneale'

class DrinkStaticMiddleware(object):
    def process_request(self, request):
        self.set_nodes(request)
        self.set_archived_nodes(request)
        self.set_live_node_groups(request)
        self.set_all_node_groups(request)
        self.set_archived_node_groups(request)

    def set_nodes(self, request):
        key = 'drinkstatic_nodes'
        nodes = None #memcache.get(key)
        if not nodes:
            nodes = NodeList(list(Node.query().filter(Node.v_archived==False)))
            memcache.set(key, nodes, time=settings.DRINKSTATIC_MEMCACHE_TIME)

        request.drinkstatic_nodes = nodes

    def set_archived_nodes(self, request):
        key = 'drinkstatic_archived_nodes'
        nodes = None #memcache.get(key)
        if not nodes:
            nodes = NodeList(list(Node.query().filter(Node.v_archived==True)))
            memcache.set(key, nodes, time=settings.DRINKSTATIC_MEMCACHE_TIME)

        request.drinkstatic_archived_nodes = nodes

    def set_live_node_groups(self, request):
        key = 'drinkstatic_live_node_groups'
        node_groups = None #memcache.get(key)
        if not node_groups:
            nodes = list(NodeGroup.query().filter(NodeGroup.group_type==NodeGroup.NodeGroupType.live))
            memcache.set(key, nodes, time=settings.DRINKSTATIC_MEMCACHE_TIME)

        request.drinkstatic_live_node_groups = node_groups

    def set_all_node_groups(self, request):
        key = 'drinkstatic_all_node_groups'
        node_groups = None #memcache.get(key)
        if not node_groups:
            nodes = list(NodeGroup.query().filter(NodeGroup.group_type==NodeGroup.NodeGroupType.all_nodes))
            memcache.set(key, nodes, time=settings.DRINKSTATIC_MEMCACHE_TIME)

        request.drinkstatic_all_node_groups = node_groups

    def set_archived_node_groups(self, request):
        key = 'drinkstatic_archived_node_groups'
        node_groups = None #memcache.get(key)
        if not node_groups:
            nodes = list(NodeGroup.query().filter(NodeGroup.group_type==NodeGroup.NodeGroupType.archived))
            memcache.set(key, nodes, time=settings.DRINKSTATIC_MEMCACHE_TIME)

        request.drinkstatic_archived_node_groups = node_groups