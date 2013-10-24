from django.http import Http404, HttpResponse
from django.conf import settings
from django.views.generic.base import TemplateView, RedirectView, View, TemplateResponseMixin
from django.template import Template
from django.template.context import Context
from drinkstatic.response import DrinkStaticTemplateResponse

__author__ = 'davneale'

class NodeView(TemplateView):

    def get(self, request, url_slug=None, *args, **kwargs):
        node = request.drinkstatic_nodes.get_by_slug(url_slug)

        if not node: raise Http404

        return DrinkStaticTemplateResponse(request, url_slug)

get_node = NodeView.as_view()

class RedirectToHome(RedirectView):
    """
    This redirect is called when the settings.BLOG_URL is called without a blog slug.
    This url should really link to a page in the site - add a url expression in your main app to override this
    """
    url = '/'

redirect_to_home = RedirectToHome.as_view()

class SitemapXMLView(TemplateResponseMixin, View):
    template = '<?xml version="1.0" encoding="UTF-8"?>'\
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'\
                    '{% for node in nodes.list %}'\
                        '<url>'\
                            '<loc>{{ root_uri }}{{ blog_url }}/{{ node.slug }}</loc>'\
                            '<priority>0.5</priority>'\
                            '<lastmod>{{ node.datestamp|date:"Y-m-d" }}</lastmod>'\
                        '</url>'\
                    '{% endfor %}'\
                '</urlset>'

    def get(self, *args, **kwargs):
        context = {
            'root_uri' : self.request.build_absolute_uri('/'),
            'blog_url' : settings.BLOG_URL,
            'nodes' : self.request.drinkstatic_nodes
        }

        template = Template(self.template)
        return HttpResponse(content=template.render(Context(context)), content_type='application/xml')

sitemap_xml = SitemapXMLView.as_view()

def cron_generator(request):
    generator_class = settings.DRINKSTATIC_GENERATOR
    generator = generator_class(request)
    generator.generate_all_nodes()

    return HttpResponse('done')