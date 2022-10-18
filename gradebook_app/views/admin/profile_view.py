from csv import DictReader
from io import TextIOWrapper

from django.http import HttpResponse

from gradebook_app.models.profile_model import Profile


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
        return HttpResponse("successful")
    except Exception as e:
        print(e)
        return HttpResponse("failed"+str(e))


def add_profile():
    pass


def update_profile():
    pass


def delete_profile():
    pass
