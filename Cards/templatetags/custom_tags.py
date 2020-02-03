from django import template
import markdown as md
import bleach
from bleach_whitelist import markdown_tags, markdown_attrs

register = template.Library()


@register.filter(name='get_class')
def get_class(value):
    return value.__class__.__name__


@register.filter()
def markdown(value):
    tags = markdown_tags
    tags.append('pre')
    return bleach.clean(md.markdown(value, extensions=['markdown.extensions.fenced_code']), tags, markdown_attrs)
