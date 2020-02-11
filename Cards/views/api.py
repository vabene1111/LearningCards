import time
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.db.models.functions import Trunc
from django.http import HttpResponse, JsonResponse
from django.utils import timezone, formats

from Cards.models import QuestionLog


def make_response_dict(qs, df):
    response = {'labels': [], 'data_success': [], 'data_failure': []}
    for i, e in enumerate(qs):
        date = formats.date_format(e['time_range'], format=df, use_l10n=True)
        response['labels'].append(date)
        response['data_success'].append(e['count_success'])
        response['data_failure'].append(e['count_failure'])

    return response


@login_required
def success_chart(request, pk):
    week = timezone.now() - timedelta(days=7)

    success_log = QuestionLog.objects.filter(user=request.user, question__course__pk=pk, created_at__gt=week).annotate(time_range=Trunc('created_at', 'hour')).values(
        'time_range').annotate(count_success=Count('id', filter=Q(type=QuestionLog.SUCCESS)), count_failure=Count('id', filter=Q(type=QuestionLog.FAIL))).order_by('time_range')

    return JsonResponse(make_response_dict(success_log, 'SHORT_DATETIME_FORMAT'))


@login_required
def all_time_chart(request, pk):
    log = QuestionLog.objects.filter(user=request.user, question__course__pk=pk).annotate(time_range=Trunc('created_at', 'day')).values(
        'time_range').annotate(count_success=Count('id', filter=Q(type=QuestionLog.SUCCESS)), count_failure=Count('id', filter=Q(type=QuestionLog.FAIL))).order_by('time_range')

    return JsonResponse(make_response_dict(log, 'SHORT_DATE_FORMAT'))


@login_required
def radar_chart(request, pk):
    log = QuestionLog.objects.filter(user=request.user, question__course__pk=pk).values('question__chapter__name').annotate(count_total=Count('id'),
                                                                                                                            count_success=Count('id', filter=Q(type=QuestionLog.SUCCESS)),
                                                                                                                            count_failure=Count('id', filter=Q(type=QuestionLog.FAIL)))

    response = {'labels': [], 'data_success': [], 'data_failure': []}
    for i, e in enumerate(log):
        percent_per_question = 100/e['count_total']
        response['labels'].append(e['question__chapter__name'])
        response['data_success'].append(round(e['count_success'] * percent_per_question))
        response['data_failure'].append(round(e['count_failure'] * percent_per_question))

    return JsonResponse(response)
