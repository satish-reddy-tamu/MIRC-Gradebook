import pandas as pd
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from gradebook_app.models import Course
from gradebook_app.models import Evaluation
from gradebook_app.models import Marks
from gradebook_app.models.common_classes import ProfileType
from gradebook_app.models.evaluation_model import EvaluationForm, GradeFunctionForm


def student_dashboard(request, profile):
    courses = profile.courses.all()
    profile_id = profile.id
    profile_first_name = profile.first_name
    current_score = [66, 85, 79,90]
    projected_score = [70, 88,81, 92]
    projected_grade = ['C','B','B','A']
    mean = [73,90,85,93]
    max = [88,92,96,100]
    zipped = list(zip(courses,current_score,projected_score, projected_grade,mean,max))

    return render(request, f"student/home.html", {
        'courses': courses,
        'profile_id': profile_id,
        'profile_first_name': profile_first_name,

        # 'current_score': current_score,
        # 'projected_score': projected_score,
        # 'projected_grade': projected_grade,
        # 'max': max,
        # 'mean': mean,
        'zipped': zipped

    })


def view_course_details(request, course_id, profile_id):
    evaluations = []
    course = Course.objects.get(id=course_id)

    try:
        evaluations = Evaluation.objects.filter(course_id=course_id).all()
    except Exception as e:
        messages.error(request, "Failed to load evaluation list: " + str(e))

    return render(request, "student/course_dashboard.html", {
        'course': course,
        'evaluations': evaluations
    })
