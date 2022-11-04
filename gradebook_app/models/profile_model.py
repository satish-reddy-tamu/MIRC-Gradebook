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

    def __str__(self):
        return self.first_name[0:7] + f" ({self.email})"


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'type', 'first_name', 'last_name', 'department', 'phone', 'date_added']


class AllocateCourseToStudentsForm(forms.Form):
    students = forms.ModelChoiceField(queryset=Profile.objects.filter(type=ProfileType.STUDENT.value).all())
    students_csv = forms.FileField()
    professors = forms.ModelChoiceField(queryset=Profile.objects.filter(type=ProfileType.PROFESSOR.value).all())
    professors_csv = forms.FileField()
