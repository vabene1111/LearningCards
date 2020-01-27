from django.urls import path

from .views import *

urlpatterns = [
    path('', views.index, name='index'),

    path('quiz/<int:pk>', views.quiz, name='quiz'),

    path('quiz/s/<int:pk>', views.quiz_success, name='quiz_success'),
    path('quiz/f/<int:pk>', views.quiz_fail, name='quiz_fail'),

    path('new/question/', new.QuestionCreate.as_view(), name='new_question'),

    # path('list/question', lists.keyword, name='list_keyword'),

    path('edit/question/<int:pk>/', edit.QuestionUpdate.as_view(), name='edit_question'),

    path('redirect/delete/<slug:name>/<int:pk>/', edit.delete_redirect, name='redirect_delete'),

    path('delete/recipe/<int:pk>/', edit.QuestionDelete.as_view(), name='delete_question'),

]
