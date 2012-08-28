from django.http import Http404
from django.conf import settings
from django.views.generic.base import TemplateView

__author__ = 'davneale'

class NodeView(TemplateView):

    def get(self, request, url_slug=None, *args, **kwargs):
        node = request.drinkstatic_nodes.get_by_slug(url_slug)

        if not node: raise Http404
        self.template_name = node.template_path
        return super(NodeView, self).get(request, *args, **kwargs)

get_node = NodeView.as_view()

if hasattr(settings, 'NODE_GET_CONTEXT_DATA'):
    NodeView.get_context_data = settings.NODE_GET_CONTEXT_DATA