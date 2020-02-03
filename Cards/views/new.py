import re

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView

from Cards.forms import *
from Cards.models import *


class QuestionCreate(LoginRequiredMixin, CreateView):
    template_name = "generic/new_template.html"
    model = Question
    form_class = QuestionForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()

        messages.add_message(self.request, messages.SUCCESS, _('Question saved! You can view it here <a href={}>here</a>').format(reverse('edit_question', kwargs={'pk': obj.pk})))
        url = reverse('new_question') + '?course=' + str(obj.course.pk)
        if obj.chapter:
            url = url + '&chapter=' + str(obj.chapter.pk)
        return HttpResponseRedirect(url)

    def get_success_url(self):
        return reverse('new_question')

    def get_context_data(self, **kwargs):
        context = super(QuestionCreate, self).get_context_data(**kwargs)
        context['title'] = _("Question")

        context['default_course'] = -1
        course = self.request.GET.get('course')
        if course:
            if re.match(r'^([1-9])+$', course):
                if Course.objects.filter(pk=int(course)).exists():
                    context['default_course'] = int(course)

        chapter = self.request.GET.get('chapter')
        if chapter:
            if re.match(r'^([1-9])+$', chapter):
                if Chapter.objects.filter(pk=int(chapter)).exists():
                    context['default_chapter'] = int(chapter)

        return context


class CourseCreate(LoginRequiredMixin, CreateView):
    template_name = "generic/new_template.html"
    model = Course
    form_class = CourseForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        return HttpResponseRedirect(reverse('edit_course', kwargs={'pk': obj.pk}))

    def get_success_url(self):
        return reverse('edit_course', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(CourseCreate, self).get_context_data(**kwargs)
        context['title'] = _("Course")
        return context


class ChapterCreate(LoginRequiredMixin, CreateView):
    template_name = "generic/new_template.html"
    model = Chapter
    form_class = ChapterForm

    def get_success_url(self):
        return reverse('edit_chapter', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ChapterCreate, self).get_context_data(**kwargs)
        context['title'] = _("Chapter")
        return context
