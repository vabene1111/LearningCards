from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.db.models.functions import Trunc
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from Cards.models import QuestionLog


@login_required
def success_chart(request, pk):
    week = timezone.now() - timedelta(days=7)

    success_log = QuestionLog.objects.filter(user=request.user, question__course__pk=pk, created_at__gt=week).annotate(time_range=Trunc('created_at', 'hour')).values(
        'time_range', 'type').annotate(count_failure=Count('id', filter=Q(type=QuestionLog.FAIL)), count_success=Count('id', filter=Q(type=QuestionLog.SUCCESS))).values('time_range', 'count_success', 'count_failure')

    response = {'labels': [], 'data_success': [], 'data_failure': []}
    for e in success_log:
        response['labels'].append(e['time_range'])
        response['data_success'].append(e['count_success'])
        response['data_failure'].append(e['count_failure'])

    return JsonResponse(response)
