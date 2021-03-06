from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django_tables2 import RequestConfig

from Cards.forms import SelectCourseForm
from Cards.helper import create_new_test, finish_test_question
from Cards.models import *
from Cards.tables import TestTable


def test_success(request, pk):
    question = TestQuestion.objects.get(pk=pk)

    if question.test.user != request.user:
        return HttpResponseRedirect(reverse('index'))

    finish_test_question(request.user, question, QuestionLog.SUCCESS)

    return HttpResponseRedirect(reverse('test', args=[question.test.pk]))


def test_fail(request, pk):
    question = TestQuestion.objects.get(pk=pk)

    if question.test.user != request.user:
        return HttpResponseRedirect(reverse('index'))

    finish_test_question(request.user, question, QuestionLog.FAIL)

    return HttpResponseRedirect(reverse('test', args=[question.test.pk]))


@login_required
def test(request, pk):
    test = Test.objects.get(pk=pk)

    if test.user != request.user:
        return HttpResponseRedirect(reverse('index'))

    tq = TestQuestion.objects.filter(test=test, type__isnull=True).order_by('?').first()

    if not tq:
        test.completed = True
        test.save()
        return HttpResponseRedirect(reverse('test_stats', args=[test.pk]))

    success_url = reverse('test_success', args=[tq.pk])
    failure_url = reverse('test_fail', args=[tq.pk])

    test_progress = {'questions': TestQuestion.objects.filter(test=test).count(),
                     'questions_done': TestQuestion.objects.filter(test=test, type__isnull=False).count()}
    test_progress['questions_progress'] = (100 / test_progress['questions'] * test_progress['questions_done']) + 1

    comments = Comment.objects.filter(question=tq.question).all()

    logs = QuestionLog.objects.filter(question=tq.question, user=request.user).order_by('created_at').all()
    if len(logs) > 0:
        log_percent = 100 / len(logs)
    else:
        log_percent = 100

    return render(request, "test.html",
                  {'question': tq.question, 'test': test, 'test_progress': test_progress, 'comments': comments,
                   'logs': logs, 'log_percent': log_percent, 'success_url': success_url, 'failure_url': failure_url})


@login_required
def test_overview(request):
    table = TestTable(Test.objects.filter(user=request.user).order_by('-created_at').all())
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    course_form = SelectCourseForm(request.user)

    return render(request, "test_overview.html", {'tests': table, 'course_form': course_form})


@login_required
def test_stats(request, pk):
    test = Test.objects.get(pk=pk)

    if test.user != request.user:
        return HttpResponseRedirect(reverse('index'))

    failed_questions = TestQuestion.objects.filter(test=test, type=QuestionLog.FAIL)
    successfull_questions = TestQuestion.objects.filter(test=test, type=QuestionLog.SUCCESS)

    return render(request, "test_stats.html",
                  {'test': test, 'failed_questions': failed_questions, 'successfull_questions': successfull_questions})


@login_required
def test_start(request, pk):
    course = Course.objects.get(pk=pk)
    if not course:
        messages.add_message(request, messages.ERROR, _('There was an error finding the selected course!'))
        return redirect("test_overview")

    test = create_new_test(request.user, course)

    return HttpResponseRedirect(reverse('test', args=[test.pk]))
