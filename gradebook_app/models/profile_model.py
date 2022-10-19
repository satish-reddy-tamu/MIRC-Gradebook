from enum import Enum

from django import forms
from django.db import models


class ProfileType(Enum):
    STUDENT = "student"
    PROFESSOR = "professor"
    STAFF = "staff"
    ADMIN = "admin"

    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)

    @classmethod
    def get_all_profiles(cls):
        return [i.value for i in cls]


class Profile(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=ProfileType.choices())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
