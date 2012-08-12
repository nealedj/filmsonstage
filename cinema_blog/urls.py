
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="home.html")),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"),  name="about"),

    url(r'^4u-fishguard/$', TemplateView.as_view(template_name="cinemas/fishguard.html"), name="4u-fishguard"),
    # Example:
    # (r'^cinema_blog/', include('cinema_blog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
