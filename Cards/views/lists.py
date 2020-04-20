from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.shortcuts import render
from django.urls import reverse_lazy
from django_tables2 import RequestConfig
from django.utils.translation import gettext as _

from Cards.filters import QuestionFilter, CourseFilter, ChapterFilter
from Cards.models import Question, Course, Chapter
from Cards.tables import QuestionTable, CourseTable, ChapterTable


@login_required
def question(request):
    f = QuestionFilter(request.GET, queryset=Question.objects.all().order_by('pk'))

    table = QuestionTable(f.qs)
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    return render(request, 'generic/list_template.html',
                  {'title': _("Questions"), 'table': table, 'create_url': 'new_question', 'filter': f})


def course(request):
    f = CourseFilter(request.GET, queryset=Course.objects.all().order_by('pk'))

    table = CourseTable(f.qs)
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    return render(request, 'generic/list_template.html',
                  {'title': _("Course"), 'table': table, 'create_url': 'new_course', 'filter': f})


@login_required
def chapter(request):
    f = ChapterFilter(request.GET, queryset=Chapter.objects.all().order_by('pk'))

    table = ChapterTable(f.qs)
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    return render(request, 'generic/list_template.html',
                  {'title': _("Chapter"), 'table': table, 'create_url': 'new_chapter', 'filter': f})
