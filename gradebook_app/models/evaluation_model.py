import datetime

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from gradebook_app.models.course_model import Course


class Evaluation(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    eval_type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    weight = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    max_marks = models.FloatField()


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['name', 'eval_type', 'weight', 'max_marks']

class GradeFunctionForm(forms.Form):
    A = forms.IntegerField()
    B = forms.IntegerField()
    C = forms.IntegerField()
    D = forms.IntegerField()
    E = forms.IntegerField()
    F = forms.IntegerField()