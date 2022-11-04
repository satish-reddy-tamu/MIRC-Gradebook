from csv import DictReader
from io import TextIOWrapper

from django.http import HttpResponse
from django.shortcuts import redirect, render

from gradebook_app.models.profile_model import Profile
from gradebook_app.models.course_model import Course

def display_all_students(request, course):
    students = course.profiles.all()
    return render(request, 'professor/studentlist.html', {
        'students': students
    })

# def get_students(request):
   
#     course_id = request.POST.get("course")
 
#     # Students enroll to Course
#     # Getting all data from course model based on course_id
#     subject_model = Subjects.objects.get(id=subject_id)
 
#     session_model = SessionYearModel.objects.get(id=session_year)
 
#     students = Students.objects.filter(course_id=subject_model.course_id,
#                                        session_year_id=session_model)
 
#     # Only Passing Student Id and Student Name Only
#     list_data = []
 
#     for student in students:
#         data_small={"id":student.admin.id,
#                     "name":student.admin.first_name+" "+student.admin.last_name}
#         list_data.append(data_small)
 
#     return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)
 
 
