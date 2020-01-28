import random
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Value, IntegerField
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from Cards.forms import CommentForm, RegisterForm
from Cards.models import *


def index(request):
    courses = Course.objects.annotate(num_questions=Count('question')).all()

    return render(request, 'index.html', {'courses': courses})


def choose_question(request, course):
    questions = Question.objects.filter(course=course).annotate(weight=Value(0, output_field=IntegerField())).order_by("-weight").all()

    if len(questions) == 0:
        return None

    if request.user.is_authenticated:
        for q in questions:

            last_log = QuestionLog.objects.filter(user=request.user, question=q).all().last()
            if last_log:
                recent = timezone.now() - last_log.created_at

                if recent.seconds < 900:
                    q.weight = q.weight - (9 - recent.seconds / 100)
            else:
                q.weight = q.weight + 5

            daily = timezone.now() - timedelta(hours=6)
            log_daily = QuestionLog.objects.filter(user=request.user, question=q, created_at__gt=daily).all()
            for ld in log_daily:
                if ld.type == QuestionLog.FAIL:
                    q.weight = q.weight + 2
                else:
                    q.weight = q.weight - 2

            log_total = QuestionLog.objects.filter(user=request.user, question=q).all()
            for lt in log_total:
                if lt.type == QuestionLog.FAIL:
                    q.weight = q.weight + 0.5
                else:
                    q.weight = q.weight - 0.5

        pool = [questions[0]]
        for q in questions:
            if q.weight > pool[0].weight:
                pool = [q]
            elif q.weight == pool[0].weight:
                pool.append(q)

        return random.choice(pool)
    else:
        return questions.order_by("?").first()


def quiz(request, pk, q=None):
    course = Course.objects.get(pk=pk)
    if q:
        question = Question.objects.get(pk=q)
    else:
        question = choose_question(request, pk)

    if q and not question:
        messages.add_message(request, messages.ERROR, _('The requested question could not be found!'))
        return HttpResponseRedirect(reverse('index'))

    if not question:
        messages.add_message(request, messages.ERROR, _('There are no questions in this course yet!'))
        return HttpResponseRedirect(reverse('index'))

    comments = Comment.objects.filter(question=question).all()

    return render(request, 'quiz.html', {'question': question, 'course': course, 'comments': comments})


def log_question(user, question, type):
    log = QuestionLog()
    log.user = user
    log.question = question
    log.type = type
    log.save()


def quiz_success(request, pk):
    question = Question.objects.get(pk=pk)
    if request.user.is_authenticated:
        log_question(request.user, question, QuestionLog.SUCCESS)
    return HttpResponseRedirect(reverse('quiz', args=[question.course.pk]))


def quiz_fail(request, pk):
    question = Question.objects.get(pk=pk)
    if request.user.is_authenticated:
        log_question(request.user, question, QuestionLog.FAIL)

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

    return render(request, "stats.html", {'global_stats': global_stats})


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
