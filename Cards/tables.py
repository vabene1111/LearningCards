import django_tables2 as tables
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django_tables2.utils import A  # alias for Accessor

from .models import *


class QuestionTable(tables.Table):
    id = tables.LinkColumn('edit_question', args=[A('id')])

    class Meta:
        model = Question
        template_name = 'generic/table_template.html'
        fields = ('id', 'question', 'course', 'author')
