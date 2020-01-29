from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _

from Cards.forms import CommentForm, RegisterForm, SelectCourseForm
from Cards.helper import finish_question, get_next_question, get_weighted_questions
from Cards.models import *


def index(request):
    courses = Course.objects.annotate(num_questions=Count('question')).filter(num_questions__gt=0).all()

    return render(request, 'index.html', {'courses': courses})


def quiz_weight_debug(request, pk):
    cache = QuestionCache.objects.filter(user=request.user, question__course=pk).all()
    weights = get_weighted_questions(request, pk)

    return render(request, 'test.html', {'weights': weights, 'cache': cache})


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
    logs = QuestionLog.objects.filter(question=question, user=request.user).all()
    log_percent = 100/len(logs)

    return render(request, 'quiz.html', {'question': question, 'course': course, 'comments': comments, 'logs': logs, 'log_percent': log_percent})


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
