from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from gradebook_app.models.profile_model import Profile
from gradebook_app.util.enums_util import ProfileType
from gradebook_app.views.professor.dashboard_view import professor_dashboard
from gradebook_app.views.student.student_dashboard_view import student_dashboard

def home(request):
    try:
        user = User.objects.get(id=request.user.id)
        if user.is_authenticated:
            return redirect(login)
        else:
            return render(request, "common/home.html")
    except User.DoesNotExist:
        return render(request, "common/home.html")


def login(request):
    user = User.objects.get(id=request.user.id)
    user_email = user.email

    try:
        profile = Profile.objects.get(email=user_email)
        if profile.type in ProfileType.get_all_profiles():
            if profile.type == ProfileType.PROFESSOR.value:
                return professor_dashboard(request, profile)
            elif profile.type == ProfileType.STUDENT.value:
                return student_dashboard(request, profile)
            else:
                return render(request, f"{profile.type}/home.html")
        else:
            return render(request, "common/access_denied.html")
    except Profile.DoesNotExist:
        messages.error(request, f'{user_email} dosenot exist')
        return render(request, "common/profile_not_exists.html")
