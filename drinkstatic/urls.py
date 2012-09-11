from django.conf import settings
from django.conf.urls.defaults import *
from drinkstatic import views


__author__ = 'davneale'

blog_url = getattr(settings, 'BLOG_URL', '')

urlpatterns = patterns('',
    url(r'^%s/(?P<url_slug>[-\w\d]+)/$' % blog_url, views.get_node,  name="drinkstatic-node"),
    url(r'^%s/sitemap.xml$' % blog_url, views.sitemap_xml,  name="drinkstatic-sitemapxml"),
    url(r'^_generate_drinkstatic_nodes/$', views.cron_generator,  name="drinkstatic-generate"),


    url(r'^%s/$' % blog_url, views.redirect_to_home, name="drinkstatic_redirect"),
)