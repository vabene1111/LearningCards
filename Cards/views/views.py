from django.shortcuts import render

# Create your views here.
from Cards.models import *


def index(request):
    courses = Course.objects.all()

    return render(request, 'index.html', {'courses': courses})


def quiz(request, pk):
    question = Question.objects.filter(course=pk).first()

    return render(request, 'quiz.html', {'question': question})
