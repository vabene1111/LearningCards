from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class Institution(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Course(models.Model):
    V_PUBLIC = 'PUBLIC'
    V_NON_PUBLIC = 'V_NON_PUBLIC'

    name = models.CharField(max_length=128)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    users = models.ManyToManyField(User, related_name='course_users')

    course_password = models.CharField(max_length=128, default='', blank=True)
    visibility = models.CharField(max_length=128, choices=((V_PUBLIC, _('Public')), (V_NON_PUBLIC, _('Not Public'))), default=V_PUBLIC)

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

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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

    def __str__(self):
        return str(self.test) + ' - ' + str(self.question)


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_by) + ' - ' + str(self.text)


class RegistrationKey(models.Model):
    key = models.CharField(max_length=32)
    info = models.TextField()
    valid_until = models.DateTimeField()

    def __str__(self):
        return f'Key: {self.key} -- Info: {self.info}'


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    signup_key = models.ForeignKey(RegistrationKey, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return str(self.user)
