from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render

from gradebook_app.models.profile_model import Profile, ProfileType


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
            return render(request, f"{profile.type}/home.html")
        else:
            return render(request, "common/access_denied.html")
    except Profile.DoesNotExist:
        return render(request, "common/profile_not_exists.html")
