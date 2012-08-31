from django.conf import settings
from django.conf.urls.defaults import *
from drinkstatic import views


__author__ = 'davneale'

blog_url = getattr(settings, 'BLOG_URL', '')

urlpatterns = patterns('',
    url(r'^%s/(?P<url_slug>[-\w\d]+)/$' % blog_url, views.get_node,  name="drinkstatic-node"),

)