from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, DeleteView

from Cards.forms import *
from Cards.models import *


class QuestionUpdate(LoginRequiredMixin, UpdateView):
    template_name = "generic/edit_template.html"
    model = Question
    form_class = QuestionForm

    # TODO add msg box
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (obj.author == request.user or request.user.is_superuser):
            messages.add_message(request, messages.ERROR, _('You cannot edit this question!'))
            return HttpResponseRedirect(reverse('index'))
        return super(QuestionUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('edit_question', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(QuestionUpdate, self).get_context_data(**kwargs)
        context['title'] = _("Question")
        return context


class CommentUpdate(LoginRequiredMixin, UpdateView):
    template_name = "generic/edit_template.html"
    model = Comment
    form_class = CommentForm

    # TODO add msg box

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (obj.created_by == request.user or request.user.is_superuser):
            messages.add_message(request, messages.ERROR, _('You cannot edit this comment!'))
            return HttpResponseRedirect(reverse('index'))  # TODO return to quiz page
        return super(CommentUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('edit_comment', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(CommentUpdate, self).get_context_data(**kwargs)
        context['title'] = _("Comment")
        return context


class CourseUpdate(LoginRequiredMixin, UpdateView):
    template_name = "generic/edit_template.html"
    model = Course
    form_class = CourseForm

    # TODO add msg box

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (obj.created_by == request.user or request.user.is_superuser):
            messages.add_message(request, messages.ERROR, _('You cannot edit this course!'))
            return HttpResponseRedirect(reverse('index'))
        return super(CourseUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('edit_course', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(CourseUpdate, self).get_context_data(**kwargs)
        context['title'] = _("Course")
        return context


class ChapterUpdate(LoginRequiredMixin, UpdateView):
    template_name = "generic/edit_template.html"
    model = Chapter
    form_class = ChapterForm

    def get_success_url(self):
        return reverse('edit_chapter', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ChapterUpdate, self).get_context_data(**kwargs)
        context['title'] = _("Chapter")
        return context


# Generic Delete views

def delete_redirect(request, name, pk):
    return redirect(('delete_' + name), pk)


class QuestionDelete(LoginRequiredMixin, DeleteView):
    template_name = "generic/delete_template.html"
    model = Question
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(QuestionDelete, self).get_context_data(**kwargs)
        context['title'] = _("Question")
        return context


class CommentDelete(LoginRequiredMixin, DeleteView):
    template_name = "generic/delete_template.html"
    model = Comment
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(CommentDelete, self).get_context_data(**kwargs)
        context['title'] = _("Comment")
        return context


class CourseDelete(LoginRequiredMixin, DeleteView):
    template_name = "generic/delete_template.html"
    model = Course
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(CourseDelete, self).get_context_data(**kwargs)
        context['title'] = _("Course")
        return context


class ChapterDelete(LoginRequiredMixin, DeleteView):
    template_name = "generic/delete_template.html"
    model = Chapter
    success_url = reverse_lazy('list_chapter')

    def get_context_data(self, **kwargs):
        context = super(ChapterDelete, self).get_context_data(**kwargs)
        context['title'] = _("Chapter")
        return context
