from csv import DictReader
from io import TextIOWrapper

from django.http import HttpResponse
from django.shortcuts import redirect, render

from gradebook_app.models.profile_model import Profile, ProfileForm


def display_all_profiles(request):
    profiles = Profile.objects.all()
    return render(request, 'admin/profiles.html', {'profiles': profiles})


def add_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect(display_all_profiles)
            except:
                pass
    else:
        form = ProfileForm()
    return render(request, 'admin/add_profile.html', {'profile_form': form})


def add_bulk_profiles(request):
    try:
        if request.method == "POST":
            profiles_csv_file = TextIOWrapper(request.FILES['profiles_csv_file'], encoding=request.encoding)
            profiles_list = []
            for row in DictReader(profiles_csv_file):
                profile = Profile(
                    email=row['email'],
                    name=row['name'],
                    type=row['type']
                )
                profiles_list.append(profile)
            Profile.objects.bulk_create(profiles_list)
            return redirect(display_all_profiles)
        else:
            return render(request, 'admin/add_bulk_profiles.html')
    except Exception as e:
        print(e)
        return HttpResponse("failed" + str(e))


def update_profile(request, id):
    profile = Profile.objects.get(id=id)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
        return redirect(display_all_profiles)
    else:
        form = ProfileForm(instance=profile)
        return render(request, 'admin/update_profile.html', {'profile_form': form, 'profile': profile})


def delete_profile(request, id):
    profile = Profile.objects.get(id=id)
    profile.delete()
    return redirect(display_all_profiles)
