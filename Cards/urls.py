from django.urls import path

from .views import *

urlpatterns = [
    path('', views.index, name='index'),

    path('quiz/<int:pk>', views.quiz, name='quiz'),
    path('quiz/<int:pk>/q/<int:q>', views.quiz, name='quiz_question'),
    path('quiz/<int:pk>/c/<int:c>', views.quiz, name='quiz_chapter'),

    path('quiz/s/<int:pk>', views.quiz_success, name='quiz_success'),
    path('quiz/f/<int:pk>', views.quiz_fail, name='quiz_fail'),

    path('quiz/s/<int:pk>/c/<int:c>', views.quiz_success, name='quiz_chapter_success'),
    path('quiz/f/<int:pk>/c/<int:c>', views.quiz_fail, name='quiz_chapter_fail'),

    path('quiz/comment/<int:pk>', views.quiz_comment, name='quiz_comment'),

    path('quiz/<int:pk>/debug/', views.quiz_weight_debug, name='quiz_debug'),  # debugging for weighting algorithm

    path('stats/', views.stats, name='stats'),

    path('test/overview/', views.test_overview, name='test_overview'),
    path('test/start/<int:pk>', views.test_start, name='test_start'),
    path('test/stats/<int:pk>', views.test_stats, name='test_stats'),

    path('test/<int:pk>', views.test, name='test'),
    path('test/s/<int:pk>', views.test_success, name='test_success'),
    path('test/f/<int:pk>', views.test_fail, name='test_fail'),

    path('new/question/', new.QuestionCreate.as_view(), name='new_question'),
    path('new/course/', new.CourseCreate.as_view(), name='new_course'),
    path('new/chapter/', new.ChapterCreate.as_view(), name='new_chapter'),

    path('list/question', lists.question, name='list_question'),
    path('list/course', lists.course, name='list_course'),
    path('list/chapter', lists.chapter, name='list_chapter'),

    path('edit/question/<int:pk>/', edit.QuestionUpdate.as_view(), name='edit_question'),
    path('edit/comment/<int:pk>/', edit.CommentUpdate.as_view(), name='edit_comment'),
    path('edit/course/<int:pk>/', edit.CourseUpdate.as_view(), name='edit_course'),
    path('edit/chapter/<int:pk>/', edit.ChapterUpdate.as_view(), name='edit_chapter'),

    path('redirect/delete/<slug:name>/<int:pk>/', edit.delete_redirect, name='redirect_delete'),

    path('delete/recipe/<int:pk>/', edit.QuestionDelete.as_view(), name='delete_question'),
    path('delete/comment/<int:pk>/', edit.CommentDelete.as_view(), name='delete_comment'),
    path('delete/course/<int:pk>/', edit.CourseDelete.as_view(), name='delete_course'),
    path('delete/chapter/<int:pk>/', edit.ChapterDelete.as_view(), name='delete_chapter'),

    path('register', views.register, name='register'),

    path('api/success_chart/<int:pk>', api.success_chart, name='api_success_chart'),
]
