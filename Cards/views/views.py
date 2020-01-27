from django.db.models import Count, F, Value, IntegerField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime, timedelta

from django.urls import reverse

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

            daily = datetime.now() - timedelta(hours=24)
            log_daily = QuestionLog.objects.filter(user=request.user, question=q, created_at__lt=daily).all()
            for ld in log_daily:
                if ld.type == QuestionLog.FAIL:
                    q.weight = q.weight + 2
                else:
                    q.weight = q.weight - 2

            total = datetime.now() - timedelta(hours=24)
            log_total = QuestionLog.objects.filter(user=request.user, question=q, created_at__lt=total).all()
            for lt in log_total:
                if lt.type == QuestionLog.FAIL:
                    q.weight = q.weight + 0.5
                else:
                    q.weight = q.weight - 0.5

        question = questions[0]
        for q in questions:
            if q.weight > question.weight:
                question = q

        return question
    else:
        return questions.order_by("?").first()


def quiz(request, pk):
    course = Course.objects.get(pk=pk)
    return render(request, 'quiz.html', {'question': choose_question(request, pk), 'course': course})


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
