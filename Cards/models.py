from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class University(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=128)
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, null=True)
    semester = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    name = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.course) + ' : ' + self.name


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT, blank=True, null=True)
    question = models.TextField()
    answer = models.TextField()
    source = models.CharField(max_length=256, null=True, blank=True)
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
        return str(self.created_at) + ' - ' + str(self.user) + ' - ' + str(self.question)


class QuestionCache(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + ' - ' + str(self.question)


class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + ' - ' + str(self.created_at) + ' - ' + str(self.course)


class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    type = models.CharField(choices=QuestionLog.STATUS_TYPES, max_length=128, blank=True, null=True)


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
