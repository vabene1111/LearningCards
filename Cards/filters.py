import django_filters

from Cards.forms import SelectWidget
from Cards.models import Question, Course, Chapter, University


class QuestionFilter(django_filters.FilterSet):
    question = django_filters.CharFilter(lookup_expr='icontains')
    course = django_filters.ModelChoiceFilter(widget=SelectWidget, queryset=Course.objects.all())
    chapter = django_filters.ModelChoiceFilter(widget=SelectWidget, queryset=Chapter.objects.all())

    class Meta:
        model = Question
        fields = ['question', 'course', 'chapter']


class CourseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    semester = django_filters.CharFilter(lookup_expr='icontains')
    university = django_filters.ModelChoiceFilter(widget=SelectWidget, queryset=University.objects.all())

    class Meta:
        model = Course
        fields = ['name', 'university', 'semester']


class ChapterFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    course = django_filters.ModelChoiceFilter(widget=SelectWidget, queryset=Course.objects.all())

    class Meta:
        model = Chapter
        fields = ['name', 'course']

