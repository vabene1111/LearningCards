from django.contrib import admin

from Cards.models import *


class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')

    @staticmethod
    def name(obj):
        return obj.user.first_name + ' ' + obj.user.last_name


class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'question', 'type', 'test_id')

    @staticmethod
    def name(obj):
        return obj.test.user.first_name + ' ' + obj.test.user.last_name


class QuestionLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'question', 'created_at')

    @staticmethod
    def name(obj):
        return obj.user.first_name + ' ' + obj.user.last_name


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text', 'question_id', 'created_at')

    @staticmethod
    def name(obj):
        return obj.created_by.first_name + ' ' + obj.created_by.last_name

    @staticmethod
    def question_id(obj):
        return obj.question.id


class RegistrationKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'info', 'valid_until')


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'signup_key')

    @staticmethod
    def name(obj):
        return obj.user.first_name + ' ' + obj.user.last_name


admin.site.register(University)
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(QuestionLog, QuestionLogAdmin)
admin.site.register(QuestionCache)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(TestQuestion, TestQuestionAdmin)
admin.site.register(RegistrationKey, RegistrationKeyAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
