from google.appengine.api import memcache
from drinkstatic.models import Node, NodeList
from django.conf import settings

__author__ = 'davneale'

class DrinkStaticMiddleware(object):
    def process_request(self, request):
        key = 'drinkstatic_nodes'
        nodes = None #memcache.get(key)
        if not nodes:
            nodes = NodeList(list(Node.query()))
            memcache.set(key, nodes, time=settings.DRINKSTATIC_MEMCACHE_TIME)

        request.drinkstatic_nodes = nodes