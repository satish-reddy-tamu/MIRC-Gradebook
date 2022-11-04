import csv
from io import TextIOWrapper

from django.http import HttpResponse
from django.shortcuts import redirect, render

from gradebook_app.models.course_model import Course, CourseForm
from gradebook_app.models.Enrollment import EnrollmentForm, Enrollment
from gradebook_app.models.profile_model import Profile

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


def update_course(request, id):
    course = Course.objects.get(id=id)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
        return redirect(display_all_courses)
    else:
        form = CourseForm(instance=course)
        return render(request, 'admin/update_course.html', {'course_form': form, 'course': course})


def delete_course(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    return redirect(display_all_courses)


def getStudentList(form, request):
    students = []
    studentEmail = form.cleaned_data['student_email']
    if studentEmail != '':
        students = [studentEmail]
    
    try:
        file = request.FILES['file']
        file_data = file.read().decode("utf-8")
        lines = file_data.split("\n")
        for line in lines:	
            line = line.rstrip()
            if line != '':
                students.append(str(line))
    except:
        print("file upload error")
    print(students)
    return students

def enrollStudents(course, students):
    for student in students:
        try:
            profile = Profile.objects.get(email=student)
            # print("ex", Enrollment.objects.filter(profile=profile, course=course).exists())
            if not Enrollment.objects.filter(profile=profile, course=course).exists():
                enrollment = Enrollment(profile=profile, course=course)
                enrollment.save()
            else:
                print("exists")
        except Exception as e: 
            print(e)
            print("save failed")


def add_students(request, id):
    course = Course.objects.get(id=id)
    print(course.id)
    if request.method == "POST":
        form = EnrollmentForm(request.POST, request.FILES)
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
        f = EnrollmentForm(auto_id=False)
        return render(request, 'admin/add_students.html', {'enrollment_form': f, 'course_id': course.id})
