from django.contrib.auth.mixins import LoginRequiredMixin
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

    def get_success_url(self):
        return reverse('edit_question', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(QuestionUpdate, self).get_context_data(**kwargs)
        context['title'] = _("Question")
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

