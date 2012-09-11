from django.conf import settings
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

__author__ = 'davneale'


def get_basic_generator():
    from drinkstatic.generator import BasicGenerator
    return BasicGenerator

DEFAULT_SETTINGS = {
    'DRINKSTATIC_MEMCACHE_TIME': 60,
    'BLOG_URL' : 'blogs',
    'DRINKSTATIC_TEMPLATE_DIRS' : (os.path.join(settings.TEMPLATE_DIRS, '/blogs'),),
    'ROOT_URLCONF' : 'cinema_blog.urls',
    'TEMPLATE_CONTEXT_PROCESSORS' : TEMPLATE_CONTEXT_PROCESSORS + ('drinkstatic.context_processors.drinkstatic',),
    'PUBLIC_CACHE_TIME' : 60,
    'NODE_LIST_LIMIT' : 8,
    'DRINKSTATIC_GENERATOR' : get_basic_generator,
    'MAX_SNIPPET_LENGTH' : 200,
}

for setting, value in DEFAULT_SETTINGS.items():
    if not hasattr(settings, setting):
        try:
            resolved_value = value()
        except TypeError:
            resolved_value = value
        setattr(settings, setting, resolved_value)
