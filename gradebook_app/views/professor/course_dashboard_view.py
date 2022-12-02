from django.shortcuts import render

from gradebook_app.models import Course


def view_course_details(request, id):
    courses = Course.objects.all()
    return render(request, "professor/course_details.html", {
        'course_id': id,
        'courses': courses
    })
