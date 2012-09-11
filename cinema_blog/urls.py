
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.views.generic.base import TemplateView
from cinema_blog import views

urlpatterns = patterns('',
    url(r'^$', views.TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"),  name="about"),

    url(r'^sitemap.xml$',  views.sitemap_xml_view, name='sitemap-xml'),
    url(r'^sitemapindex.xml', views.sitemapindex_xml_view, name='sitemap-index-xml'),

    (r'', include('drinkstatic.urls'),),
)
