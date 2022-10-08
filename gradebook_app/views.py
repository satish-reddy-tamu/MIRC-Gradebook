from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render
import random

# Create your views here.
from django.http import HttpResponse

from gradebook_app.models import User


def index(request):
    return HttpResponse("Hello, world. You're at the gradebook app index.")


def getAllUsers(request):
    lst = User.objects.all()
    print(len(lst))
    return 0


def getUser(request, email):
    user = User.objects.get(email=email)
    if user.type == 1:
        return render(request, "student_home.html")
    elif user.type == 2:
        return render(request, "teacher_home.html")


def addUser(request, email):
    userTypes = [1, 2]
    user = User(email=email, type = random.choice(userTypes))
    user.save()
    return user.email