from django import template
import markdown as md
import bleach
from bleach_whitelist import markdown_tags, markdown_attrs, all_styles

register = template.Library()


@register.filter(name='get_class')
def get_class(value):
    return value.__class__.__name__


@register.filter()
def markdown(value):
    tags = markdown_tags + ['pre', 'table', 'td', 'tr', 'th', 'tbody', 'style']
    return bleach.clean(md.markdown(value, extensions=['markdown.extensions.fenced_code']), tags, markdown_attrs, all_styles)
