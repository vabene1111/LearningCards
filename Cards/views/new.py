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
        return HttpResponseRedirect(reverse('new_question'))

    def get_success_url(self):
        return reverse('new_question')

    def get_context_data(self, **kwargs):
        context = super(QuestionCreate, self).get_context_data(**kwargs)
        context['title'] = _("Question")
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
