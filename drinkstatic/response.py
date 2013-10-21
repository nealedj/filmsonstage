from django.template.response import TemplateResponse
from django.conf import settings
from django.template import Template as DjangoTemplate
from django.views.decorators.cache import patch_cache_control
from google.appengine.api import memcache
from drinkstatic.models import Template

__author__ = 'davneale'

class DrinkStaticTemplateResponse(TemplateResponse):

    def __init__(self, request, template, *args, **kwargs):

        super(DrinkStaticTemplateResponse, self).__init__(request, template, *args, **kwargs)

        patch_cache_control(
            self, public=True,
            max_age=settings.PUBLIC_CACHE_TIME,
        )
        self['Pragma'] = 'Public'

    def resolve_template(self, template):
        src = memcache.get(template)
        if not src:
            src = Template.get_by_template_key(template)
            memcache.set(template, src)
        return DjangoTemplate(src.source)


