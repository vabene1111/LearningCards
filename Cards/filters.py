import django_filters

from Cards.models import Question


class QuestionFilter(django_filters.FilterSet):
    question = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Question
        fields = ['question', 'course', 'chapter']
