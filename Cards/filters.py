import django_filters

from Cards.models import Question, Course


class QuestionFilter(django_filters.FilterSet):
    question = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Question
        fields = ['question', 'course', 'chapter']


class CourseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    semester = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Course
        fields = ['name', 'university', 'semester']
