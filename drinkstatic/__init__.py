from django.conf import settings
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
from collections import OrderedDict

__author__ = 'davneale'


def get_basic_generator():
    from drinkstatic.generator import BasicGenerator
    return BasicGenerator

DEFAULT_SETTINGS = OrderedDict(
    DRINKSTATIC_MEMCACHE_TIME=60,
    BLOG_URL='blogs',
    ROOT_URLCONF='cinema_blog.urls',
    DRINKSTATIC_TEMPLATE_DIRS=(os.path.join(settings.TEMPLATE_DIRS, '/blogs'),),
    DRINKSTATIC_THUMBNAIL_DIR=os.path.join(os.path.dirname(__file__), '../static/img/cinemas'),
    TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS + ('drinkstatic.context_processors.drinkstatic',),
    PUBLIC_CACHE_TIME=60,
    NODE_LIST_LIMIT=8,
    MAX_SNIPPET_LENGTH=200,
    THUMBNAIL_WIDTH=150,
)

DEFAULT_SETTINGS['DRINKSTATIC_GENERATOR'] = get_basic_generator

for setting, value in DEFAULT_SETTINGS.items():
    if not hasattr(settings, setting):
        try:
            resolved_value = value()
        except TypeError:
            resolved_value = value
        setattr(settings, setting, resolved_value)
