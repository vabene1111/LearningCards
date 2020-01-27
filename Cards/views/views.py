from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from Cards.models import *


def index(request):
    courses = Course.objects.annotate(num_questions=Count('question')).all()

    return render(request, 'index.html', {'courses': courses})


def quiz(request, pk):
    question = Question.objects.filter(course=pk).first()

    return render(request, 'quiz.html', {'question': question})


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
