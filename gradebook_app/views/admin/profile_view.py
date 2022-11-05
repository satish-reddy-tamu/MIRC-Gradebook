from csv import DictReader
from io import TextIOWrapper

from django.http import HttpResponse
from django.shortcuts import redirect, render

from gradebook_app.models.profile_model import Profile, ProfileForm, Course, AllocateCourseToStudentsForm
from gradebook_app.models.course_model import Course, CourseForm

def display_all_courses(request):
    courses = Course.objects.all()
    return render(request, 'admin/courses.html', {
        'courses': courses,
        'add_course_form': CourseForm(),
        'assign_course_to_profile_form': AllocateCourseToStudentsForm()
    })

def display_all_profiles(request):
    profiles = Profile.objects.all()
    return render(request, 'admin/profiles.html', {
        'profiles': profiles,
        'add_profile_form': ProfileForm()
    })


def add_profile(request):
    print("heer-----------")
    form = ProfileForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            return redirect(display_all_profiles)
        except:
            print("save failed")
    else:
        print("invalid form")


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
        return redirect(display_all_profiles)
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