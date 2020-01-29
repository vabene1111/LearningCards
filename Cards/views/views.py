from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django_tables2 import RequestConfig

from Cards.forms import CommentForm, RegisterForm, SelectCourseForm
from Cards.helper import finish_question, get_next_question, get_weighted_questions, create_new_test, finish_test_question
from Cards.models import *
from Cards.tables import TestTable


def index(request):
    courses = Course.objects.annotate(num_questions=Count('question')).filter(num_questions__gt=0).all()

    return render(request, 'index.html', {'courses': courses})


def quiz_weight_debug(request, pk):
    cache = QuestionCache.objects.filter(user=request.user, question__course=pk).all()
    weights = get_weighted_questions(request, pk)

    return render(request, 'debug.html', {'weights': weights, 'cache': cache})


def quiz(request, pk, q=None):
    course = Course.objects.get(pk=pk)
    if q:
        question = Question.objects.get(pk=q)
    else:
        question = get_next_question(request, pk)

    if q and not question:
        messages.add_message(request, messages.ERROR, _('The requested question could not be found!'))
        return HttpResponseRedirect(reverse('index'))

    if not question:
        messages.add_message(request, messages.ERROR, _('There are no questions in this course yet!'))
        return HttpResponseRedirect(reverse('index'))

    comments = Comment.objects.filter(question=question).all()

    if request.user.is_authenticated:
        logs = QuestionLog.objects.filter(question=question, user=request.user).all()
        if len(logs) > 0:
            log_percent = 100 / len(logs)
        else:
            log_percent = 100
    else:
        logs = None
        log_percent = None

    success_url = reverse('quiz_success', args=[question.pk])
    failure_url = reverse('quiz_fail', args=[question.pk])

    return render(request, 'quiz.html', {'question': question, 'course': course, 'comments': comments, 'logs': logs, 'log_percent': log_percent, 'success_url': success_url, 'failure_url': failure_url})


def quiz_success(request, pk):
    question = Question.objects.get(pk=pk)
    if request.user.is_authenticated:
        finish_question(request.user, question, QuestionLog.SUCCESS)
    return HttpResponseRedirect(reverse('quiz', args=[question.course.pk]))


def quiz_fail(request, pk):
    question = Question.objects.get(pk=pk)
    if request.user.is_authenticated:
        finish_question(request.user, question, QuestionLog.FAIL)

    return HttpResponseRedirect(reverse('quiz', args=[question.course.pk]))


@login_required
def quiz_comment(request, pk):
    question = Question.objects.get(pk=pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comment()
            comment.question = question
            comment.text = comment_form.cleaned_data['text']
            comment.created_by = request.user

            comment.save()
        else:
            messages.add_message(request, messages.ERROR, _('There was an error saving your comment!') + str(comment_form.errors))

    return HttpResponseRedirect(reverse('quiz', args=[question.course.pk]))


@login_required
def stats(request):
    global_stats = {}
    global_stats['number_questions'] = Question.objects.count()
    global_stats['number_questions_played'] = QuestionLog.objects.filter(user=request.user).count()
    global_stats['number_questions_success'] = QuestionLog.objects.filter(user=request.user, type=QuestionLog.SUCCESS).count()
    global_stats['number_questions_failure'] = QuestionLog.objects.filter(user=request.user, type=QuestionLog.FAIL).count()
    global_stats['number_questions_success_percent'] = 100 / global_stats['number_questions_played'] * global_stats['number_questions_success']
    global_stats['number_questions_failure_percent'] = 100 / global_stats['number_questions_played'] * global_stats['number_questions_failure']

    course_form = SelectCourseForm()

    return render(request, "stats.html", {'global_stats': global_stats, 'course_form': course_form})


def test_success(request, pk):
    question = TestQuestion.objects.get(pk=pk)
    finish_test_question(request.user, question, QuestionLog.SUCCESS)

    return HttpResponseRedirect(reverse('test', args=[question.test.pk]))


def test_fail(request, pk):
    question = TestQuestion.objects.get(pk=pk)
    finish_test_question(request.user, question, QuestionLog.FAIL)

    return HttpResponseRedirect(reverse('test', args=[question.test.pk]))


@login_required
def test(request, pk):
    test = Test.objects.get(pk=pk)
    tq = TestQuestion.objects.filter(test=test, type__isnull=True).order_by('?').first()

    if not tq:
        test.completed = True
        test.save()
        return HttpResponseRedirect(reverse('test_stats', args=[test.pk]))

    success_url = reverse('test_success', args=[tq.pk])
    failure_url = reverse('test_fail', args=[tq.pk])

    test_progress = {'questions': TestQuestion.objects.filter(test=test).count(), 'questions_done': TestQuestion.objects.filter(test=test, type__isnull=False).count()}
    test_progress['questions_progress'] = 100 / test_progress['questions'] * test_progress['questions_done']

    return render(request, "test.html", {'question': tq.question, 'test': test, 'test_progress': test_progress, 'success_url': success_url, 'failure_url': failure_url})


@login_required
def test_overview(request):
    table = TestTable(Test.objects.filter(user=request.user).order_by('created_at').all())
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    course_form = SelectCourseForm()

    return render(request, "test_overview.html", {'tests': table, 'course_form': course_form})


@login_required
def test_stats(request, pk):
    test = Test.objects.get(pk=pk)

    failed_questions = TestQuestion.objects.filter(test=test, type=QuestionLog.FAIL)
    successfull_questions = TestQuestion.objects.filter(test=test, type=QuestionLog.SUCCESS)

    return render(request, "test_stats.html", {'test': test, 'failed_questions': failed_questions, 'successfull_questions': successfull_questions})


@login_required
def test_start(request, pk):
    course = Course.objects.get(pk=pk)
    if not course:
        messages.add_message(request, messages.ERROR, _('There was an error finding the selected course!'))
        return redirect("test_overview")

    test = create_new_test(request.user, course)

    return HttpResponseRedirect(reverse('test', args=[test.pk]))


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)

        return redirect("index")
    else:
        form = RegisterForm()

    return render(request, "registration/signup.html", {"form": form})
