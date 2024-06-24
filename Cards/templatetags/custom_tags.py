from django import template
import markdown as md
import bleach
from markdown.extensions.tables import TableExtension

from Cards.helper.mdx_extension import MarkdownFormatExtension
from Cards.helper.mdx_urlize import UrlizeExtension

register = template.Library()


@register.filter(name='get_class')
def get_class(value):
    return value.__class__.__name__


@register.filter()
def markdown(value):
    tags = {
        "h1", "h2", "h3", "h4", "h5", "h6",
        "b", "i", "strong", "em", "tt",
        "p", "br",
        "span", "div", "blockquote", "code", "pre", "hr",
        "ul", "ol", "li", "dd", "dt",
        "img",
        "a",
        "sub", "sup",
        'pre', 'table', 'td', 'tr', 'th', 'tbody', 'style', 'thead'
    }
    parsed_md = md.markdown(
        value,
        extensions=[
            'markdown.extensions.fenced_code', TableExtension(),
            UrlizeExtension(), MarkdownFormatExtension()
        ]
    )
    markdown_attrs = {
        "*": ["id", "class", 'width', 'height'],
        "img": ["src", "alt", "title"],
        "a": ["href", "alt", "title"],
    }

    return bleach.clean(parsed_md, tags, markdown_attrs)
