from django.conf import settings
from django.conf.urls.defaults import *
from drinkstatic import views


__author__ = 'davneale'


urlpatterns = patterns('',
    url(r'^%s/(?P<url_slug>[-\w\d]+)/$' % settings.BLOG_URL, views.get_node,  name="drinkstatic-node"),

)