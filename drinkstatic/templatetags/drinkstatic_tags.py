import datetime
from django import template
from django.template import Node
import sys
from drinkstatic import node_types

__author__ = 'davneale'

register = template.Library()

class DrinkStaticNode(template.Node):
    def __init__(self, node_type, node, to_render):
        self.node_type = node_type
        self.node = node
        self.to_render= to_render

    def render(self, context):
        if self.to_render:
            if isinstance(self.node, Node):
                return self.node.render(context)
            else:
                return self.node

    def get_value(self, context):
        """Used for node generator"""
        if isinstance(self.node, Node):
            return self.node.render(context)
        return self.node

    def is_unique_on_page(self):
        if self.node_type == node_types.TITLE_TEXT:
            return True

        return False

def drinkstatic_block_tag(parser, token, node_type, endblock_tag):
    try:
        token_ar = token.split_contents()
        render = True
        if len(token_ar) == 2:
            render = token_ar[1]
        nodelist = parser.parse((endblock_tag,))
        parser.delete_first_token()
        return DrinkStaticNode(node_type, nodelist[0], render)
    except (ValueError):
        raise template.TemplateSyntaxError(
            'could not parse %s') % node_type

def drinkstatic_tag(parser, token, node_type, parser_fn=None):
    token_ar = token.split_contents()
    value = token_ar[1].replace('"', '').replace("'", "")

    render = True
    if len(token_ar) == 3:
        render = token_ar[2]

    if parser_fn:
        value = parser_fn(value)

    return DrinkStaticNode(node_type, value, render)

@register.tag
def titletext(parser, token):
    return drinkstatic_block_tag(parser, token, node_types.TITLE_TEXT, 'endtitletext')

@register.tag
def datestamp(parser, token):
    return drinkstatic_tag(parser, token, node_types.DATESTAMP, lambda d: datetime.datetime.strptime(d, '%Y-%m-%d'))

@register.tag
def thumbnail(parser, token):
    return drinkstatic_tag(parser, token, node_types.THUMBNAIL)

@register.tag
def urlslug(parser, token):
    return drinkstatic_tag(parser, token, node_types.URL_SLUG)

@register.tag
def snippet(parser, token):
    return drinkstatic_block_tag(parser, token, node_types.SNIPPET, 'endsnippet')

@register.tag
def archived(parser, token):
    return DrinkStaticNode(node_types.ARCHIVED, True, False)
