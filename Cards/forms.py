from django import forms
from django.contrib.auth.forms import UserCreationForm
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


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Making location required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2"]
