from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from gradebook_app.models import Profile
from django.contrib.auth.models import User

def index(request):
    return HttpResponse("Hello, world. You're at the gradebook app index.")

def login(request):
    user = User.objects.get(id=request.user.id)
    user_email = user.email
    user = Profile.objects.get(email=user_email)
    if user.type == 1:
        return render(request, "student_home.html")
    elif user.type == 2:
        return render(request, "teacher_home.html")


def getUser(request, email):
    user = Profile.objects.get(email=email)
    if user.type == 1:
        return render(request, "student_home.html")
    elif user.type == 2:
        return render(request, "teacher_home.html")
