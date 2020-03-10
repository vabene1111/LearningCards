from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from fpdf import FPDF, HTMLMixin

from Cards.models import Question, Course, Chapter
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def export_course(request, pk):
    course = get_object_or_404(Course, pk)
    chapter = Chapter.objects.filter(course=course)
    questions = Question.objects.filter(course=course).all()

    q = {}

    return render_to_pdf('export_question_pdf.html', {'questions': questions})
