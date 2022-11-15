from django.http import HttpResponse
from django.shortcuts import render, redirect

from gradebook_app.models import Course, Evaluation
from gradebook_app.models.common_classes import ProfileType
from gradebook_app.models.evaluation_model import EvaluationForm, GradeFunctionForm


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


def evaluations_list(request, id):
    evaluations = []
    try:
        evaluations = Evaluation.objects.filter(course_id=id).all()
    except Exception as e:
        print(e)
    return render(request, 'professor/evaluations_list.html', {
        'evaluations': evaluations,
        'course_id': id
    })


evaluations = {}
eval_id = 1
grade_function = ""


def add_evaluation(request, id):
    global eval_id
    form = EvaluationForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        e = Evaluation(id=eval_id,
                       name=cleaned_data.get("name"),
                       eval_type=cleaned_data.get("eval_type"),
                       weight=cleaned_data.get('weight'),
                       max_marks=cleaned_data.get("max_marks"))
        evaluations[e.id] = e
        eval_id += 1
        return redirect(configure_course, id=id)
    else:
        print("invalid form")


# def update_evaluation(request, eval_id):
#     evaluation = evaluations.get(eval_id)
#     if request.method == "POST":
#         form = EvaluationForm(request.POST, instance=evaluation)
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             e = Evaluation(id=eval_id,
#                            name=cleaned_data.get("name"),
#                            eval_type=cleaned_data.get("eval_type"),
#                            weight=cleaned_data.get('weight'),
#                            max_marks=cleaned_data.get("max_marks"))
#             evaluations[e.id] = e
#         else:
#             print("Invalid Form")
#     else:
#         form = EvaluationForm(request.POST, instance=evaluation)
#         return render(request, "")

def delete_evaluation(request, course_id, eval_id):
    evaluations.pop(eval_id)
    return redirect(configure_course, id=course_id)


def configure_course(request, id):
    sum_ = sum(value.weight for key, value in evaluations.items())
    return render(request, f"professor/configure_course.html",
                  {'local_evaluations': evaluations.values(),
                   'add_evaluation_form': EvaluationForm(),
                   'sum': sum_,
                   'grade_function_form': GradeFunctionForm(),
                   'grade_function': grade_function,
                   'course_id': id})


def add_course_configuration(request, id):
    global eval_id, grade_function
    evaluation_objs = []
    for eval in evaluations.values():
        print(eval.name, eval.eval_type, eval.weight, eval.max_marks, id)
        evaluation_objs.append(Evaluation(
            name=eval.name,
            eval_type=eval.eval_type,
            weight=eval.weight,
            max_marks=eval.max_marks,
            course_id=id
        )
        )
    print(evaluation_objs)
    Evaluation.objects.bulk_create(evaluation_objs)
    Course.objects.filter(id=id).update(thresholds=grade_function)
    evaluations.clear()
    eval_id =1
    grade_function = ""
    return HttpResponse("Success")

def add_grade_function(request, id):
    global grade_function
    form = GradeFunctionForm(request.POST)
    if form.is_valid():
        thresholds = []
        thresholds.append(form.cleaned_data.get("A"))
        thresholds.append(form.cleaned_data.get("B"))
        thresholds.append(form.cleaned_data.get("C"))
        thresholds.append(form.cleaned_data.get("D"))
        thresholds.append(form.cleaned_data.get("E"))
        thresholds.append(form.cleaned_data.get("F"))
        thresholds = list(map(int, thresholds))
        if thresholds == sorted(thresholds, reverse=True):
            thresholds = list(map(str, thresholds))
            grade_function = ",".join(thresholds)
        else:
            print("Wrong values")
    return redirect(configure_course, id=id)

