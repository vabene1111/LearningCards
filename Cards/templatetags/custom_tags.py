from django import template
import markdown as md
import bleach
from bleach_whitelist import markdown_tags, markdown_attrs

from Cards.helper.mdx_extension import MarkdownFormatExtension

register = template.Library()


@register.filter(name='get_class')
def get_class(value):
    return value.__class__.__name__


@register.filter()
def markdown(value):
    tags = markdown_tags + ['pre', 'table', 'td', 'tr', 'th', 'tbody', 'style', 'thead']
    parsed_md = md.markdown(value, extensions=['markdown.extensions.fenced_code', 'tables', MarkdownFormatExtension()])
    return bleach.clean(parsed_md, tags, markdown_attrs)

