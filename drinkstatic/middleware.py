from google.appengine.api import memcache
from drinkstatic import generator

__author__ = 'davneale'

class DrinkStaticMiddleware(object):
    def process_request(self, request):
        key = 'drinkstatic_nodes'
        nodes = None # memcache.get(key)
        if not nodes:
            nodes = generator.get_all_nodes()
            memcache.set(key, nodes)

        request.drinkstatic_nodes = nodes