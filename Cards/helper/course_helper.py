from django.utils.translation import gettext as _

from Cards.models import *
from Cards.tables import QuestionTable


def get_chapters(course):
    chapters = {}

    for ch in course.chapter_set.all():
        chapters[ch.pk] = {
            'name': ch.name,
            'table': QuestionTable(Question.objects.filter(chapter=ch).order_by('pk').all())
        }

    if Question.objects.filter(chapter=None, course=course).order_by('pk').all().count() > 0:
        chapters['No_Chapter'] = {
            'name': _("No Chapter"),
            'table': QuestionTable(Question.objects.filter(chapter=None, course=course).order_by('pk').all())
        }

    return chapters
