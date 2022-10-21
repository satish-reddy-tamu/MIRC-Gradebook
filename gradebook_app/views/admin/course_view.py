from csv import DictReader
from io import TextIOWrapper

from django.http import HttpResponse
from django.shortcuts import redirect, render

from gradebook_app.models.course_model import Course, CourseForm

def display_all_courses(request):
    courses = Course.objects.all()
    return render(request, 'admin/courses.html', {
        'courses': courses,
        'add_course_form': CourseForm()
    })


def add_course(request):
    form = CourseForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            return redirect(display_all_courses)
        except:
            print("save failed")
    else:
        print("invalid form")


def update_course():
    pass


def delete_course():
    pass
