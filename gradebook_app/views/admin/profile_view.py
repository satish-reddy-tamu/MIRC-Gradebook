from csv import DictReader
from gradebook_app.models.profile_model import Profile


def add_bulk_profiles(request):
    try:
        profiles_csv_file = request.FILES["profiles_csv_file"]
        profiles_list = []
        for row in DictReader(profiles_csv_file):
            profile = Profile(
                email=row['email'],
                name=row['name'],
                type=row['type']
            )
            profiles_list.append(profile)
        Profile.objects.bulk_create(profiles_list)
    except Exception as e:
        print(e)


def add_profile():
    pass


def update_profile():
    pass


def delete_profile():
    pass
