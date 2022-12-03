from django.contrib import messages
from django.db.models import Avg, Max, Min, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from gradebook_app.forms.evaluation_form import EvaluationForm
from gradebook_app.forms.grade_function_form import GradeFunctionForm
from gradebook_app.forms.student_evaluations_edit_form import EvaluationEditForm
from gradebook_app.forms.student_evaluations_upload_form import EvaluationsUploadForm
from gradebook_app.models import Course
from gradebook_app.models import Evaluation
from gradebook_app.models import Marks
from gradebook_app.models.profile_model import ProfileCourse, Profile
from gradebook_app.util.enums_util import ProfileType


def professor_dashboard(request, profile):
    courses = profile.courses.all()
    return render(request, f"professor/home.html", {'courses': courses})


def view_course_details(request, id):
    x = ProfileCourse.objects.filter(
        course_id=id,
        profile__type=ProfileType.STUDENT.value)
    y = x.aggregate(
        Avg('score'), Max('score'), Min('score')
    )
    top_students = x.order_by('-score')[:5].values('profile__first_name', 'profile__email', 'score')
    bottom_students = x.order_by('score')[:5].values('profile__first_name', 'profile__email', 'score')
    d = x.values('grade').annotate(count=Count('grade')).order_by('count')

    grades = []
    numbers = []
    for query in d:
        grades.append(query['grade'])
        numbers.append(query['count'])
    for key, value in y.items():
        if value:
            y[key] = round(value, 2)
        else:
            y[key] = 0.0
    course = Course.objects.filter(id=id).values('name', 'thresholds')
    thresholds = course[0].get('thresholds').split(',')
    return render(request, 'professor/course_dashboard.html', {
        'course_id': id,
        **y,
        'top_students': top_students,
        'bottom_students': bottom_students,
        'grade_distribution': d,
        'grades': grades,
        'numbers': numbers,
        'thresholds': thresholds
    })


def view_students_list(request, id):
    students = Profile.objects.filter(type=ProfileType.STUDENT.value, profilecourse__course_id=id).values(
        'id', 'first_name', 'profilecourse__score', 'profilecourse__grade'
    )
    total_evaluations = Evaluation.objects.filter(course_id=id).values(
        'id', 'name', 'max_marks'
    )
    final_evaluations = []
    for student in students:
        row = [student['id'], student['first_name']]
        for e in total_evaluations:
            graded_evaluation = Marks.objects.filter(course_id=id, profile_id=student['id'],
                                                     evaluation_id=e['id']).values(
                'evaluation_id', 'evaluation__name', 'marks'
            )
            if graded_evaluation:
                row.append(graded_evaluation[0]['marks'])
            else:
                row.append('-')
        row.extend([student['profilecourse__score'], student['profilecourse__grade']])
        final_evaluations.append(row)
    eval_choices = []
    for eval in total_evaluations:
        eval_choices.append((eval['id'], eval['name']))
    return render(request, 'professor/students_list.html', {
        'students': students,
        'course_id': id,
        'evals': total_evaluations,
        'final_evaluations': final_evaluations,
        'student_evaluations_upload_form':  EvaluationsUploadForm(evaluations=eval_choices)
    })


def update_student_evaluation(request, course_id, profile_id):
    try:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            total_evaluations = Evaluation.objects.filter(course_id=course_id).values(
                'id', 'name', 'max_marks'
            )
            final_evaluations = []
            for e in total_evaluations:
                graded_evaluation = Marks.objects.filter(course_id=course_id, profile_id=profile_id,
                                                         evaluation_id=e['id']).values('marks')
                if graded_evaluation:
                    marks = graded_evaluation[0]['marks']
                else:
                    marks = '-'
                final_evaluations.append((e['id'], e['name'], marks, e['max_marks']))
            form = EvaluationEditForm(instance=final_evaluations)
            if request.method == "POST":
                form.save(course_id, profile_id, request.POST)
                messages.success(request, f"Student ID: {profile_id} Evaluations Updated successfully")
                return JsonResponse({"form_is_valid": True})
            else:
                form = EvaluationEditForm(instance=final_evaluations)
                html_form = render_to_string("professor/student_evaluations_edit_form.html",
                                             {"course_id": course_id, "profile_id": profile_id, "edit": True,
                                              "student_evaluations_edit_form": form}, request)
                return JsonResponse({"html_form": html_form})
    except Exception as e:
        messages.error(request, f"Student ID: {profile_id} Evaluations Update failed due to: " + str(e))
        return JsonResponse({})


def evaluations_list(request, id):
    evaluations = []
    try:
        evaluations = Evaluation.objects.filter(course_id=id).all()
    except Exception as e:
        messages.error(request, "Failed to load evaluation list: " + str(e))
    finally:
        return render(request, 'professor/evaluations_list.html', {
            'evaluations': evaluations,
            'course_id': id
        })


def add_evaluation(request, id):
    try:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if request.method == "POST":
                form = EvaluationForm(request.POST)
                if form.is_valid():
                    cleaned_data = form.cleaned_data
                    e = {
                        "id": request.session['eval_id'],
                        'name': cleaned_data.get("name"),
                        "eval_type": cleaned_data.get("eval_type"),
                        "weight": cleaned_data.get("weight"),
                        "max_marks": cleaned_data.get("max_marks")
                    }
                    request.session['evaluations'][request.session['eval_id']] = e
                    request.session['eval_id'] = str(int(request.session['eval_id']) + 1)
                    request.session.modified = True
                    return JsonResponse({"form_is_valid": True})
                else:
                    html_form = render_to_string("professor/evaluation_form.html",
                                                 {"evaluation_form": form, "add": True, "course_id": id}, request)
                    return JsonResponse({"form_is_valid": False, "html_form": html_form})
            elif request.method == "GET":
                form = EvaluationForm()
                html_form = render_to_string("professor/evaluation_form.html",
                                             {"evaluation_form": form, "add": True, "course_id": id}, request)
                return JsonResponse({"html_form": html_form})
    except Exception as e:
        messages.error(request, "Evaluation Addition failed due to: " + str(e))
        return JsonResponse({})


def update_evaluation(request, course_id, eval_id):
    try:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print(request.session['evaluations'].get(str(eval_id)))
            evaluation_dict = request.session['evaluations'].get(str(eval_id))
            evaluation = Evaluation(**evaluation_dict)
            if request.method == "POST":
                form = EvaluationForm(request.POST, instance=evaluation)
                if form.is_valid():
                    cleaned_data = form.cleaned_data
                    e = {
                        "id": str(eval_id),
                        'name': cleaned_data.get("name"),
                        "eval_type": cleaned_data.get("eval_type"),
                        "weight": cleaned_data.get("weight"),
                        "max_marks": cleaned_data.get("max_marks")
                    }
                    request.session['evaluations'][str(eval_id)] = e
                    request.session.modified = True
                    return JsonResponse({"form_is_valid": True})
                else:
                    html_form = render_to_string("professor/evaluation_form.html",
                                                 {"evaluation_form": form, "update": True,
                                                  "course_id": course_id, "eval_id": eval_id},
                                                 request)
                    return JsonResponse({"form_is_valid": False, "html_form": html_form})
            elif request.method == "GET":
                form = EvaluationForm(instance=evaluation)
                html_form = render_to_string("professor/evaluation_form.html",
                                             {"evaluation_form": form, "update": True,
                                              "course_id": course_id, "eval_id": eval_id}, request)
                return JsonResponse({"html_form": html_form})
    except Exception as e:
        messages.error(request, f"Evaluation ID: {id} Update failed due to: " + str(e))
        return JsonResponse({})


def delete_evaluation(request, course_id, eval_id):
    try:
        request.session['evaluations'].pop(str(eval_id))
        request.session.modified = True
    except Exception as e:
        messages.error(request, f"Evaluation ID: {id} Deletion failed due to: " + str(e))
    finally:
        return redirect(configure_course, id=course_id)


def configure_course(request, id):
    if 'evaluations' not in request.session:
        request.session['evaluations'] = {}
    if 'eval_id' not in request.session:
        request.session['eval_id'] = 1
    if 'grade_function' not in request.session:
        request.session['grade_function'] = ""
    evals = request.session['evaluations']
    sum_ = sum(value['weight'] for key, value in evals.items())
    return render(request, f"professor/configure_course.html",
                  {'local_evaluations': evals.values(),
                   'add_evaluation_form': EvaluationForm(),
                   'sum': sum_,
                   'grade_function_form': GradeFunctionForm(),
                   'grade_function': request.session['grade_function'],
                   'course_id': id})


def add_course_configuration(request, id):
    try:
        evaluation_objs = []
        for eval in request.session['evaluations'].values():
            evaluation_objs.append(Evaluation(
                name=eval['name'],
                eval_type=eval['eval_type'],
                weight=eval['weight'],
                max_marks=eval['max_marks'],
                course_id=id
            )
            )
        Evaluation.objects.bulk_create(evaluation_objs)
        Course.objects.filter(id=id).update(thresholds=request.session['grade_function'])
        request.session['evaluations'].clear()
        request.session['eval_id'] = 1
        request.session['grade_function'] = ""
        request.session.modified = True
        messages.error(request, f"Course ID: {id} Configuration added successfully")
    except Exception as e:
        messages.error(request, f"Course ID: {id} Configuration addition failed: {str(e)}")
    finally:
        return redirect(view_course_details, id=id)


def add_grade_function(request, id):
    try:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if request.method == "POST":
                form = GradeFunctionForm(request.POST)
                if form.is_valid():
                    thresholds = [form.cleaned_data.get("A"),
                                  form.cleaned_data.get("B"),
                                  form.cleaned_data.get("C"),
                                  form.cleaned_data.get("D"),
                                  form.cleaned_data.get("E"),
                                  form.cleaned_data.get("F")
                                  ]
                    thresholds = list(map(str, thresholds))
                    request.session['grade_function'] = ",".join(thresholds)
                    request.session.modified = True
                    return JsonResponse({"form_is_valid": True})
                else:
                    html_form = render_to_string("professor/evaluation_form.html",
                                                 {"evaluation_form": form, "course_id": id}, request)
                    return JsonResponse({"form_is_valid": False, "html_form": html_form})
            elif request.method == "GET":
                form = GradeFunctionForm()
                html_form = render_to_string("professor/evaluation_form.html",
                                             {"evaluation_form": form, "course_id": id}, request)
                return JsonResponse({"html_form": html_form})
    except Exception as e:
        messages.error(request, "Grade Function Addition failed due to: " + str(e))
        return JsonResponse({})


def add_bulk_evaluations(request, id):
    try:
        form = EvaluationsUploadForm(request.POST, request.FILES)
        if request.method == "POST":
            form.save(id, request.POST, request.FILES)
    except Exception as e:
        messages.error(request, "GEvaluations Upload failed due to: " + str(e))
    finally:
        return redirect(view_students_list, id=id)
