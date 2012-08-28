__author__ = 'davneale'

def drinkstatic(request):

    context = {
        'nodes' :request.drinkstatic_nodes
    }

    return context