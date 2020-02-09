import django_filters

from Cards.models import Question


class QuestionFilter(django_filters.FilterSet):

    class Meta:
        model = Question
        fields = ['question', 'course', 'chapter']
