from django.views.generic import TemplateView

__author__ = 'david'


class HomeView(TemplateView):
    template_name = "home.html"


class AboutView(TemplateView):
    template_name = "about.html"


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
