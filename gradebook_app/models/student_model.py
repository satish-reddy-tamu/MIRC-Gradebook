from django import forms
from django.db import models

from gradebook_app.models.profile_model import Profile


class Student(Profile):
    degree = models.CharField(max_length=50)
    gpa = models.FloatField()


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
