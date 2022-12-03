from django.db.models import F, Avg, Max, Min, Sum
from django.shortcuts import render

from gradebook_app.models import Course, ProfileCourse
from gradebook_app.models import Marks
from gradebook_app.util.enums_util import ProfileType
from gradebook_app.util.marks_util import calculate_normalized_score


def student_dashboard(request, profile):
    profile_id = profile.id
    profile_first_name = profile.first_name
    courses = ProfileCourse.objects.filter(profile_id=profile_id).all().values(
        'course_id', 'course__name', 'course__course_code', 'score', 'grade'
    )

    return render(request, f"student/home.html", {
        'courses': courses,
        'profile_id': profile_id,
        'profile_first_name': profile_first_name
    })


def view_course_details(request, profile_id, course_id):
    course = Course.objects.filter(id=course_id).values('name', 'thresholds')
    thresholds = course[0].get('thresholds').split(',')

    score_grade = ProfileCourse.objects.filter(profile_id=profile_id, course_id=course_id).values('score', 'grade')
    stats = ProfileCourse.objects.filter(course_id=course_id, profile__type=ProfileType.STUDENT.value).aggregate(
        Avg('score'), Max('score'), Min('score')
    )

    weight_total = Marks.objects.filter(profile_id=profile_id,course_id=course_id).aggregate(Sum('evaluation__weight'))


    evaluations = Marks.objects.filter(profile_id=profile_id, course_id=course_id).annotate(
        score=calculate_normalized_score(F('marks'), 0, F('evaluation__max_marks')) * (F('evaluation__weight')/weight_total['evaluation__weight__sum']),
        max_score= 100 * (F('evaluation__weight')/weight_total['evaluation__weight__sum'])
    ).values(
        'marks', 'evaluation_id', 'evaluation__name', 'evaluation__eval_type', 'evaluation__weight',
        'evaluation__max_marks', 'score', 'max_score'
    )

    total = Marks.objects.filter(profile_id=profile_id, course_id=course_id).annotate(
        score=calculate_normalized_score(F('marks'), 0, F('evaluation__max_marks')) * (F('evaluation__weight') / weight_total['evaluation__weight__sum']),
        max_score=100 * (F('evaluation__weight') / weight_total['evaluation__weight__sum'])
    ).aggregate(Sum('marks'), Sum('evaluation__max_marks'), Sum('score'), Sum('max_score'))

    return render(request, "student/course_dashboard.html", {
        'stats': stats,
        'course': course,
        'thresholds': thresholds,
        'evaluations': evaluations,
        'score_grade': score_grade,
        'total': total
    })
