import csv
from io import TextIOWrapper

from django.http import HttpResponse
from django.shortcuts import redirect, render

from gradebook_app.models.course_model import Course, AdminCourseForm
from gradebook_app.models.profile_model import Profile
from gradebook_app.models.profile_model import AllocateCourseToStudentsForm

def display_all_courses(request):
    courses = Course.objects.all()
    return render(request, 'admin/courses.html', {
        'courses': courses,
        'add_course_form': AdminCourseForm(),
        'assign_course_to_profile_form': AllocateCourseToStudentsForm()
    })


def add_course(request):
    form = AdminCourseForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            return redirect(display_all_courses)
        except:
            print("save failed")
    else:
        print("invalid form")


def update_course(request, id):
    course = Course.objects.get(id=id)
    if request.method == "POST":
        form = AdminCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
        return redirect(display_all_courses)
    else:
        form = AdminCourseForm(instance=course)
        return render(request, 'admin/update_course.html', {'course_form': form, 'course': course})


def delete_course(request, id):
    course = Course.objects.get(id=id)
    course.delete()
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
    print(students+professors)
    return students+professors

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
    course = Course.objects.get(id=id)
    print(course.id)
    if request.method == "POST":
        form = AllocateCourseToStudentsForm(request.POST, request.FILES)
        if form.is_valid():
            students = getStudentList(form, request)
            try:
                enrollStudents(course, students)
                return redirect(display_all_courses)
            except Exception as e: 
                print(e)
                print("save failed")
        else:
            print("invalid form")
    else:
        f = AllocateCourseToStudentsForm(auto_id=False)
        return render(request, 'admin/add_students.html', {'enrollment_form': f, 'course_id': course.id})
