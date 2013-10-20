from google.appengine.api import memcache
from google.appengine.ext import ndb
from drinkstatic.models import Node, NodeList, NodeGroup
from django.conf import settings

__author__ = 'davneale'

class DrinkStaticMiddleware(object):
    def process_request(self, request):
        # key: (finalise, query)
        context_var_types = {
            'drinkstatic_nodes': (NodeList, lambda: Node.query().filter(Node.v_archived==False)),
            'drinkstatic_archived_nodes': (NodeList, lambda: Node.query().filter(Node.v_archived==True)),
            'drinkstatic_live_node_groups': (lambda m: m, lambda: NodeGroup.query().filter(NodeGroup.group_type==NodeGroup.NodeGroupType.live)),
            'drinkstatic_all_node_groups': (lambda m: m, lambda: NodeGroup.query().filter(NodeGroup.group_type==NodeGroup.NodeGroupType.all_nodes)),
            'drinkstatic_archived_node_groups': (lambda m: m, lambda: NodeGroup.query().filter(NodeGroup.group_type==NodeGroup.NodeGroupType.archived))
        }

        context_results = memcache.get_multi(context_var_types.keys())

        futures = {}
        for k,v in context_var_types.items():
            if k not in context_results:
                futures[k] = v[1]().fetch_async()

        ndb.Future.wait_all(futures.values())
        for k,v in futures.items():
            context_results[k] = context_var_types[k][0](list(v.get_result()))
            memcache.set(k, context_results[k], time=settings.DRINKSTATIC_MEMCACHE_TIME)

        for k,v in context_results.items():
            setattr(request, k, v)
