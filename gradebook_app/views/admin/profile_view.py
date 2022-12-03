from csv import DictReader
from io import TextIOWrapper

from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from gradebook_app.forms.profile_form import ProfileForm
from gradebook_app.models.profile_model import Profile


def display_all_profiles(request):
    try:
        profiles = Profile.objects.all()
        return render(request, 'admin/profiles.html', {
            'profiles': profiles,
            'add_profile_form': ProfileForm()
        })
    except Exception as e:
        messages.error(request, "Error loading profiles: " + str(e))
        return HttpResponse("Error loading profiles: " + str(e))


def add_profile(request):
    try:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if request.method == "POST":
                form = ProfileForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Profile Added successfully")
                    return JsonResponse({"form_is_valid": True})
                else:
                    html_form = render_to_string("admin/profile_form.html", {"profile_form": form, "add": True},
                                                 request)
                    return JsonResponse({"form_is_valid": False, "html_form": html_form})
            elif request.method == "GET":
                form = ProfileForm()
                html_form = render_to_string("admin/profile_form.html", {"profile_form": form, "add": True}, request)
                return JsonResponse({"html_form": html_form})
    except Exception as e:
        messages.error(request, "Profile Addition failed due to: " + str(e))
        return JsonResponse({})


def add_bulk_profiles(request):
    try:
        profiles_csv_file = TextIOWrapper(request.FILES['profiles_csv_file'], encoding=request.encoding)
        profiles_list = []
        for row in DictReader(profiles_csv_file):
            profile = Profile(
                email=row['email'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                department=row['department'],
                phone=row['phone'],
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
    try:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            profile = Profile.objects.get(id=id)
            if request.method == "POST":
                form = ProfileForm(request.POST, instance=profile)
                if form.is_valid():
                    form.save()
                    messages.success(request, f"Profile ID: {id} Updated successfully")
                    return JsonResponse({"form_is_valid": True})
                else:
                    html_form = render_to_string("admin/profile_form.html",
                                                 {"profile_form": form, "update": True, "profile_id": id}, request)
                    return JsonResponse({"form_is_valid": False, "html_form": html_form})
            elif request.method == "GET":
                form = ProfileForm(instance=profile)
                html_form = render_to_string("admin/profile_form.html",
                                             {"profile_form": form, "update": True, "profile_id": id}, request)
                return JsonResponse({"html_form": html_form})
    except Exception as e:
        messages.error(request, f"Profile ID: {id} Update failed due to: " + str(e))
        return JsonResponse({})


def delete_profile(request, id):
    try:
        profile = Profile.objects.get(id=id)
        profile.delete()
        messages.success(request, f"Profile ID: {id} Deleted Successfully")
    except Exception as e:
        messages.error(request, f"Profile ID: {id} Deletion failed due to: " + str(e))
    finally:
        return redirect(display_all_profiles)
