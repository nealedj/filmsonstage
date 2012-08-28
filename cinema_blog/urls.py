
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.views.generic.base import TemplateView
from cinema_blog import views

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view()),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"),  name="about"),

    url(r'^4u-fishguard/$', TemplateView.as_view(template_name="cinemas/fishguard.html"), name="4u-fishguard"),
    url(r'^royal-st-ives/$', TemplateView.as_view(template_name="cinemas/st-ives.html"), name="royal-st-ives"),
    (r'', include('drinkstatic.urls'),),
    # Example:
    # (r'^cinema_blog/', include('cinema_blog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
