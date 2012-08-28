import datetime
from django import template
from django.template import Node
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

@register.tag
def titletext(parser, token):
    try:
        token_ar = token.split_contents()
        render = True
        if len(token_ar) == 2:
            render = token_ar[1]
        nodelist = parser.parse(('endtitletext',))
        parser.delete_first_token()
    except (ValueError):
        raise template.TemplateSyntaxError(
            'could not parse title')

    return DrinkStaticNode(node_types.TITLE_TEXT, nodelist[0], render)

@register.tag
def datestamp(parser, token):
    tag_name, raw_date = token.split_contents()

    date = datetime.datetime.strptime(raw_date, '%Y-%m-%d')
    return DrinkStaticNode(node_types.DATESTAMP, date, False)

@register.tag
def thumbnail(parser, token):
    token_ar = token.split_contents()
    thumbnail = token_ar[1]

    render = True
    if len(token_ar) == 3:
        render = token_ar[2]

    return DrinkStaticNode(node_types.THUMBNAIL, thumbnail, render)
