import json
from csv import DictReader
from io import TextIOWrapper

from django.contrib import messages
from django.shortcuts import redirect, render

from gradebook_app.models.profile_model import Profile, ProfileForm


def display_all_profiles(request):
    profiles = Profile.objects.all()
    return render(request, 'admin/profiles.html', {
        'profiles': profiles,
        'add_profile_form': ProfileForm()
    })


def add_profile(request):
    try:
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Added successfully")
        else:
            for key, value in json.loads(form.errors.as_json()).items():
                message = f"{key}: "
                for val in value:
                    message += val['message']
                messages.error(request, message)
    except Exception as e:
        messages.error(request, "Profile Addition failed due to: " + str(e))
    finally:
        return redirect(display_all_profiles)


def add_bulk_profiles(request):
    try:
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
        messages.success(request, "Bulk Profiles Added Successfully")
    except Exception as e:
        messages.error(request, "Bulk Profiles Addition failed due to: " + str(e))
    finally:
        return redirect(display_all_profiles)


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
    try:
        profile = Profile.objects.get(id=id)
        profile.delete()
        messages.success(request, "Profile Deleted Successfully")
    except Exception as e:
        messages.error(request, "Profile Deletion failed due to: " + str(e))
    finally:
        return redirect(display_all_profiles)
