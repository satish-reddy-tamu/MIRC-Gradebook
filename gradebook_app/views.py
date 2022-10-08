from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from gradebook_app.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import redirect


def home(request):
    try:
        user = User.objects.get(id=request.user.id)
        if user.is_authenticated:
            return redirect(login)
        else:
            return render(request, "home.html")
    except User.DoesNotExist:
        return render(request, "home.html")


def login(request):
    user = User.objects.get(id=request.user.id)
    user_email = user.email
    try:
        profile = Profile.objects.get(email=user_email)
        if profile.type == 1:
            return render(request, "student_home.html")
        elif profile.type == 2:
            return render(request, "teacher_home.html")
    except Profile.DoesNotExist:
        return render(request, "access_denied.html")
