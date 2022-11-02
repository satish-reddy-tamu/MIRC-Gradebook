from django import forms
from django.db import models

from gradebook_app.models.profile_model import Profile


class Professor(Profile):
    title = models.CharField(max_length=50)


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = '__all__'
