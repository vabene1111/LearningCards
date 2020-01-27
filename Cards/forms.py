from django import forms
from django.forms import widgets
from django.utils.translation import gettext as _

from Cards.models import *


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('course', 'question', 'answer')
