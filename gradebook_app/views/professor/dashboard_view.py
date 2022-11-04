from django.shortcuts import render

from gradebook_app.models import Course
from gradebook_app.models.common_classes import ProfileType


def professor_dashboard(request, profile):
    courses = profile.courses.all()
    return render(request, f"professor/home.html", {'courses': courses})


def view_course_details(request, id):
    return render(request, "professor/course_details.html", {'course_id': id})


def view_students_list(request, id):
    students = []
    try:
        students = Course.objects.get(id=id).profiles.filter(type=ProfileType.STUDENT.value).all()
    except Exception as e:
        print(e)
    return render(request, 'professor/students_list.html', {
        'students': students,
        'course_id': id
    })
