__author__ = 'davneale'

def drinkstatic(request):

    context = {
        'nodes' :request.drinkstatic_nodes,
        'archived_nodes': request.drinkstatic_archived_nodes,
        'live_node_groups': request.drinkstatic_live_node_groups,
        'all_node_groups' : request.drinkstatic_all_node_groups,
        'archived_node_groups' : request.drinkstatic_archived_node_groups

    }

    return context