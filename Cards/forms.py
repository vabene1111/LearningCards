from django import forms
from django.forms import widgets
from django.utils.translation import gettext as _

from Cards.models import *


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('course', 'question', 'answer')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

        labels = {
            'text': _('Add your comment: '),
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': 15}),
        }
