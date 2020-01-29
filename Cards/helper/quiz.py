import random
from datetime import timedelta

from django.db.models import Value, IntegerField, CharField
from django.utils import timezone

from Cards.models import Question, QuestionLog, QuestionCache


def get_weighted_questions(request, course):
    questions = Question.objects.filter(course=course).annotate(weight=Value(0, output_field=IntegerField()), note=Value("", output_field=CharField())).all()

    question_list = list(questions.values())

    if len(questions) == 0:
        return None

    if not request.user.is_authenticated:
        return question_list

    for q in question_list:

        last_log = QuestionLog.objects.filter(user=request.user, question_id=q['id']).all().last()
        if last_log:
            recent = timezone.now() - last_log.created_at

            if recent.seconds < 1200:
                q['weight'] = q['weight'] - (12 - recent.seconds / 100)
                q['note'] = q['note'] + " -sec(" + str((12 - recent.seconds / 100)) + ')'
        else:
            q['weight'] = q['weight'] + 5
            q['note'] = q['note'] + " +none(5)"

        daily = timezone.now() - timedelta(hours=6)
        log_daily = QuestionLog.objects.filter(user=request.user, question_id=q['id'], created_at__gt=daily).all()
        for ld in log_daily:
            if ld.type == QuestionLog.FAIL:
                q['weight'] = q['weight'] + 2
                q['note'] = q['note'] + " +d(2)"
            else:
                q['weight'] = q['weight'] - 2
                q['note'] = q['note'] + " -d(2)"

        log_total = QuestionLog.objects.filter(user=request.user, question_id=q['id']).all()
        for lt in log_total:
            if lt.type == QuestionLog.FAIL:
                q['weight'] = q['weight'] + 0.5
                q['note'] = q['note'] + " +a(0.5)"
            else:
                q['weight'] = q['weight'] - 0.5
                q['note'] = q['note'] + " -a(0.5)"

    question_list = sorted(question_list, key=lambda i: i['weight'], reverse=True)

    return question_list


def add_cache_entry(user, question):
    cache_entry = QuestionCache()
    cache_entry.user = user
    cache_entry.question = question
    cache_entry.save()


def build_question_cache(request, course_id):
    weights = get_weighted_questions(request, course_id)

    for i, q in enumerate(weights):
        if i > 4:
            break
        question = Question.objects.get(id=q['id'])
        add_cache_entry(request.user, question)

    if len(weights) > 2:
        question = Question.objects.get(id=random.choice(weights[:len(weights) // 2])['id'])
        add_cache_entry(request.user, question)


def remove_cache_entry(user, question):
    cache_entries = QuestionCache.objects.filter(user=user, question=question).all()
    for entry in cache_entries:
        entry.delete()


def get_next_question(request, course_id):
    if not request.user.is_authenticated:
        return Question.objects.filter(course=course_id).order_by("?").first()

    cache = QuestionCache.objects.filter(user=request.user, question__course__id=course_id).all()
    if len(cache) < 2:
        build_question_cache(request, course_id)

    cache_entry = cache.first()
    if not cache_entry:
        print("No cache found for user, resorting to random question")
        return Question.objects.filter(course=course_id).order_by("?").first()

    return cache_entry.question


def finish_question(user, question, type):
    remove_cache_entry(user, question)
    log = QuestionLog()
    log.user = user
    log.question = question
    log.type = type
    log.save()
