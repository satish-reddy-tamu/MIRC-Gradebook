from django import forms
from django.core.exceptions import ValidationError
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
    A = forms.IntegerField(min_value=0, max_value=100)
    B = forms.IntegerField(min_value=0, max_value=100)
    C = forms.IntegerField(min_value=0, max_value=100)
    D = forms.IntegerField(min_value=0, max_value=100)
    E = forms.IntegerField(min_value=0, max_value=100)
    F = forms.IntegerField(min_value=0, max_value=100)

    def clean(self):
        values = list(self.cleaned_data.values())
        if values != sorted(values, reverse=True):
            raise ValidationError("Given Values are not sorted")
