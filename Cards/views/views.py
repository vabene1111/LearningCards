from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django_tables2 import RequestConfig

from Cards.forms import RegisterForm, SelectCourseForm, CourseSearchForm
from Cards.models import *
from Cards.tables import UserCourseTable


def index(request):
    courses = Course.objects.annotate(num_questions=Count('question', distinct=True),
                                      num_chapters=Count('chapter', distinct=True)).filter(
        num_questions__gt=0).order_by('name').all()
    chapters = Chapter.objects.annotate(num_questions=Count('question')).filter(num_questions__gt=0).order_by(
        'name').all()

    return render(request, 'index.html', {'courses': courses, 'chapters': chapters})


def question(request):
    return render(request, 'question.html', {})


def course(request):
    return render(request, 'course.html', {})


@login_required()
def settings(request):
    if request.method == 'POST':
        form = CourseSearchForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            course.users.add(request.user)
            course.save()

    form = CourseSearchForm()

    table = UserCourseTable(Course.objects.order_by('pk').filter(users=request.user).all())
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    return render(request, 'settings.html', {'form': form, 'table': table})


@login_required
def stats(request):
    user_stats = {}
    user_stats['number_questions_played'] = QuestionLog.objects.filter(user=request.user).count()
    user_stats['number_questions_success'] = QuestionLog.objects.filter(user=request.user,
                                                                        type=QuestionLog.SUCCESS).count()
    user_stats['number_questions_failure'] = QuestionLog.objects.filter(user=request.user,
                                                                        type=QuestionLog.FAIL).count()
    if user_stats['number_questions_played'] > 0 and user_stats['number_questions_played'] > 0:
        user_stats['number_questions_success_percent'] = 100 / user_stats['number_questions_played'] * user_stats[
            'number_questions_success']
        user_stats['number_questions_failure_percent'] = 100 / user_stats['number_questions_played'] * user_stats[
            'number_questions_failure']
    else:
        user_stats['number_questions_success_percent'] = 100
        user_stats['number_questions_failure_percent'] = 100

    global_stats = {}
    global_stats['number_questions_played'] = QuestionLog.objects.count()
    global_stats['number_questions_success'] = QuestionLog.objects.filter(type=QuestionLog.SUCCESS).count()
    global_stats['number_questions_failure'] = QuestionLog.objects.filter(type=QuestionLog.FAIL).count()
    if global_stats['number_questions_played'] > 0 and global_stats['number_questions_played'] > 0:
        global_stats['number_questions_success_percent'] = 100 / global_stats['number_questions_played'] * global_stats[
            'number_questions_success']
        global_stats['number_questions_failure_percent'] = 100 / global_stats['number_questions_played'] * global_stats[
            'number_questions_failure']
    else:
        global_stats['number_questions_success_percent'] = 100
        global_stats['number_questions_failure_percent'] = 100

    course_form = SelectCourseForm()

    return render(request, "stats.html",
                  {'user_stats': user_stats, 'global_stats': global_stats, 'course_form': course_form})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)

        return redirect("index")
    else:
        form = RegisterForm()

    return render(request, "registration/signup.html", {"form": form})
