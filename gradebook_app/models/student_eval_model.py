from django import forms
from django.db import models

from gradebook_app.models.evaluation_model import Evaluation
from gradebook_app.models.profile_model import Profile


class StudentEval(Profile, Evaluation):
    grade = models.FloatField()


class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentEval
        fields = '__all__'
