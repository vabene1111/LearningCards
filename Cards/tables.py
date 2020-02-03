import django_tables2 as tables
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django_tables2.utils import A  # alias for Accessor

from .models import *


class QuestionTable(tables.Table):
    id = tables.LinkColumn('edit_question', args=[A('id')])
    question = tables.LinkColumn('quiz_question', args=[A('id'),A('course.pk')])

    class Meta:
        model = Question
        template_name = 'generic/table_template.html'
        fields = ('id', 'question', 'course', 'author')


class CourseTable(tables.Table):
    id = tables.LinkColumn('edit_course', args=[A('id')])

    class Meta:
        model = Course
        template_name = 'generic/table_template.html'
        fields = ('id', 'name', 'university', 'semester')


class TestTable(tables.Table):
    id = tables.LinkColumn('test', args=[A('id')])
    status = tables.Column(empty_values=())

    def render_status(self, record):
        if record.completed:
            return mark_safe('<span class="badge badge-success">' + _('Complete') + '</span>')
        else:
            return mark_safe('<span class="badge badge-warning">' + _('Incomplete') + '</span>')

    class Meta:
        model = Test
        template_name = 'generic/table_template.html'
        fields = ('id', 'course', 'created_at')
