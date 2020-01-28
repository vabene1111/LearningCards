from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.shortcuts import render
from django.urls import reverse_lazy
from django_tables2 import RequestConfig
from django.utils.translation import gettext as _

from Cards.models import Question, Course
from Cards.tables import QuestionTable, CourseTable


@login_required
def question(request):
    table = QuestionTable(Question.objects.order_by('pk').all())
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    return render(request, 'generic/list_template.html', {'title': _("Questions"), 'table': table, 'create_url': 'new_question'})


@login_required
def course(request):
    table = CourseTable(Course.objects.order_by('pk').all())
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    return render(request, 'generic/list_template.html', {'title': _("Course"), 'table': table, 'create_url': 'new_course'})

