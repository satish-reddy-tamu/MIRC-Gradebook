import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect

from gradebook_app.models import Course
from gradebook_app.models import Evaluation
from gradebook_app.models import Marks
from gradebook_app.models import Profile


def view_course_details(request, id):
    courses = Course.objects.all()
    return render(request, "professor/course_details.html", {
        'course_id': id,
        'courses': courses
        })

