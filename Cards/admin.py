from django.contrib import admin

# Register your models here.
from Cards.models import *

admin.site.register(Course)
admin.site.register(Question)
admin.site.register(QuestionLog)