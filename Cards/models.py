from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class Course(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.question


class QuestionLog(models.Model):
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'
    STATUS_TYPES = ((SUCCESS, _('Success')), (FAIL, _('Fail')))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    type = models.CharField(choices=STATUS_TYPES, max_length=128, default=SUCCESS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ' - ' + str(self.question)
