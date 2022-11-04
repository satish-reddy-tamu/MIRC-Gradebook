import datetime

from django import forms
from django.db import models

from gradebook_app.models.common_classes import Departments, ProfileType
from gradebook_app.models.course_model import Course


class Profile(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    type = models.CharField(max_length=10, choices=ProfileType.choices())
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.CharField(max_length=10, choices=Departments.choices(), default="")
    phone = models.CharField(max_length=50)
    date_added = models.DateField(default=datetime.date.today)
    courses = models.ManyToManyField(Course, related_name='profiles')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email','type','first_name','last_name','department','phone','date_added']
