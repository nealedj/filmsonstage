
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.views.generic.base import TemplateView
from cinema_blog import views

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name="home"),
    url(r'^about/$', views.AboutView.as_view(),  name="about"),

    url(r'^sitemap.xml$',  views.sitemap_xml_view, name='sitemap-xml'),
    url(r'^sitemapindex.xml', views.sitemapindex_xml_view, name='sitemap-index-xml'),

    (r'', include('drinkstatic.urls'),),
)
