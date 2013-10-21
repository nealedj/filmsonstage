from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.cache import patch_cache_control

__author__ = 'david'

class CachedTemplate(TemplateView):
    def get_cache_timeout(self):
        return settings.PUBLIC_CACHE_TIME

    def dispatch(self, *args, **kwargs):
        response = super(CachedTemplate, self).dispatch(*args, **kwargs)
        patch_cache_control(response, public=True, max_age=self.get_cache_timeout())
        return response

class HomeView(CachedTemplate):
    template_name = "home.html"
home_view = HomeView.as_view()


class AboutView(CachedTemplate):
    template_name = "about.html"
about_view = AboutView.as_view()


class SitemapXML(TemplateView):
    template_name = 'sitemap.xml'

    def get_context_data(self, **kwargs):
        return {'root_uri' : self.request.build_absolute_uri('/')}

    def render_to_response(self, context, **response_kwargs):
        return self.response_class(
            request = self.request,
            template = self.get_template_names(),
            context = context,
            content_type = 'application/xml'
        )
sitemap_xml_view = SitemapXML.as_view()


class SitemapIndexXML(SitemapXML):
    template_name = 'sitemapindex.xml'
sitemapindex_xml_view = SitemapIndexXML.as_view()
