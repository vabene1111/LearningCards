from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _

from Cards.forms import CommentForm
from Cards.helper import finish_question, get_next_question, get_weighted_questions
from Cards.models import *


def quiz_weight_debug(request, pk):
    cache = QuestionCache.objects.filter(user=request.user, question__course=pk).all()
    weights = get_weighted_questions(request, pk)

    return render(request, 'debug.html', {'weights': weights, 'cache': cache})


def quiz(request, pk, q=None, c=None):
    course = Course.objects.get(pk=pk)
    chapter = Chapter.objects.filter(pk=c).first()

    if q:
        question = Question.objects.get(pk=q)
    else:
        question = get_next_question(request, pk, chapter)

    if q and not question:
        messages.add_message(request, messages.ERROR, _('The requested question could not be found!'))
        return HttpResponseRedirect(reverse('index'))

    if not question:
        messages.add_message(request, messages.ERROR, _('There are no questions in this course/chapter yet!'))
        return HttpResponseRedirect(reverse('index'))

    comments = Comment.objects.filter(question=question).all()

    if request.user.is_authenticated:
        logs = QuestionLog.objects.filter(question=question, user=request.user).order_by('created_at').all()
        if len(logs) > 0:
            log_percent = 100 / len(logs)
        else:
            log_percent = 100
    else:
        logs = None
        log_percent = None

    if chapter:
        success_url = reverse('quiz_chapter_success', args=[question.pk, c])
        failure_url = reverse('quiz_chapter_fail', args=[question.pk, c])
    else:
        success_url = reverse('quiz_success', args=[question.pk])
        failure_url = reverse('quiz_fail', args=[question.pk])

    return render(request, 'quiz.html', {'question': question, 'course': course, 'comments': comments, 'logs': logs,
                                         'log_percent': log_percent, 'success_url': success_url,
                                         'failure_url': failure_url})


def quiz_success(request, pk, c=None):
    question = Question.objects.get(pk=pk)
    finish_question(request.user, question, QuestionLog.SUCCESS)

    if c:
        return HttpResponseRedirect(reverse('quiz_chapter', args=[question.course.pk, c]))
    else:
        return HttpResponseRedirect(reverse('quiz', args=[question.course.pk]))


def quiz_fail(request, pk, c=None):
    question = Question.objects.get(pk=pk)
    finish_question(request.user, question, QuestionLog.FAIL)

    if c:
        return HttpResponseRedirect(reverse('quiz_chapter', args=[question.course.pk, c]))
    else:
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

            return HttpResponseRedirect(comment_form.cleaned_data['return_url'])
        else:
            messages.add_message(request, messages.ERROR,
                                 _('There was an error saving your comment!') + str(comment_form.errors))

    return HttpResponseRedirect(reverse('quiz', args=[question.course.pk]))
