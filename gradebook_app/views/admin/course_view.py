from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from gradebook_app.forms.course_form import AdminCourseForm, AllocateCourseToStudentsForm
from gradebook_app.models.course_model import Course
from gradebook_app.models.profile_model import Profile


def display_all_courses(request):
    try:
        courses = Course.objects.all()
        return render(request, 'admin/courses.html', {
            'courses': courses,
            'course_form': AdminCourseForm(),
            'assign_course_to_profile_form': AllocateCourseToStudentsForm()
        })
    except Exception as e:
        messages.error(request, "Error loading courses: " + str(e))
        return HttpResponse("Error loading courses: " + str(e))


def add_course(request):
    try:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if request.method == "POST":
                form = AdminCourseForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Course Added successfully")
                    return JsonResponse({"form_is_valid": True})
                else:
                    html_form = render_to_string("admin/course_form.html", {"course_form": form, "add": True}, request)
                    return JsonResponse({"form_is_valid": False, "html_form": html_form})
            elif request.method == "GET":
                form = AdminCourseForm()
                html_form = render_to_string("admin/course_form.html", {"course_form": form, "add": True}, request)
                return JsonResponse({"html_form": html_form})
    except Exception as e:
        messages.error(request, "Course Addition failed due to: " + str(e))
        return JsonResponse({})


def update_course(request, id):
    try:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            course = Course.objects.get(id=id)
            if request.method == "POST":
                form = AdminCourseForm(request.POST, instance=course)
                if form.is_valid():
                    form.save()
                    messages.success(request, f"Course ID: {id} Updated successfully")
                    return JsonResponse({"form_is_valid": True})
                else:
                    html_form = render_to_string("admin/course_form.html",
                                                 {"course_form": form, "update": True, "course_id": id}, request)
                    return JsonResponse({"form_is_valid": False, "html_form": html_form})
            elif request.method == "GET":
                form = AdminCourseForm(instance=course)
                html_form = render_to_string("admin/course_form.html",
                                             {"course_form": form, "update": True, "course_id": id}, request)
                return JsonResponse({"html_form": html_form})
    except Exception as e:
        messages.error(request, f"Course ID: {id} Update failed due to: " + str(e))
        return JsonResponse({})


def delete_course(request, id):
    try:
        course = Course.objects.get(id=id)
        course.delete()
        messages.success(request, f"Course ID: {id} Deleted Successfully")
    except Exception as e:
        messages.error(request, f"Course ID: {id} deletion failed due to: " + str(e))
    finally:
        return redirect(display_all_courses)


def getStudentList(form, request):
    students = []
    professors = []
    studentEmail = ''
    professorEmail = ''
    if form.cleaned_data['students']:
        studentEmail = form.cleaned_data['students'].email
    if studentEmail != '':
        students = [studentEmail]

    if form.cleaned_data['professors']:
        professorEmail = form.cleaned_data['professors'].email
    if professorEmail != '':
        professors = [professorEmail]

    try:
        file = request.FILES['students_csv']
        file_data = file.read().decode("utf-8")
        lines = file_data.split("\n")
        for line in lines:
            line = line.rstrip()
            if line != '':
                students.append(str(line))
    except:
        print("file upload error")

    try:
        file = request.FILES['professors_csv']
        file_data = file.read().decode("utf-8")
        lines = file_data.split("\n")
        for line in lines:
            line = line.rstrip()
            if line != '':
                students.append(str(line))
    except:
        print("file upload error")
    print(students + professors)
    return students + professors


def enrollStudents(course, students):
    for student in students:
        try:
            profile = Profile.objects.get(email=student)
            # print("ex", Enrollment.objects.filter(profile=profile, course=course).exists())
            profile.courses.add(course)
            profile.save()
        except Exception as e:
            print(e)
            print("save failed")


def enroll(request, id):
    try:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            course = Course.objects.get(id=id)
            if request.method == "POST":
                form = AllocateCourseToStudentsForm(request.POST, request.FILES)
                if form.is_valid():
                    students = getStudentList(form, request)
                    enrollStudents(course, students)
                    messages.success(request, f"Enrolled Profiles for course id: {id} successfully")
                    return JsonResponse({"form_is_valid": True})
                else:
                    html_form = render_to_string("admin/course_form.html",
                                                 {"course_form": form, "course_id": id}, request)
                    return JsonResponse({"form_is_valid": False, "html_form": html_form})
            elif request.method == "GET":
                form = AllocateCourseToStudentsForm()
                html_form = render_to_string("admin/course_form.html",
                                             {"course_form": form, "course_id": id}, request)
                return JsonResponse({"html_form": html_form})
    except Exception as e:
        messages.error(request, f"Profiles Enrollment for course id: {id} failed due to: " + str(e))
        return JsonResponse({})
