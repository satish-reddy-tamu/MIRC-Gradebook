import datetime

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from gradebook_app.models.course_model import Course


class Evaluation(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    eval_type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    weight = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    max_marks = models.IntegerField()


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = '__all__'
