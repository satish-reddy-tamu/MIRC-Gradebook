from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from gradebook_app.models.course_model import Course
from gradebook_app.util.enums_util import EvaluationTypes


class Evaluation(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    eval_type = models.CharField(max_length=20, choices=EvaluationTypes.choices())
    name = models.CharField(max_length=100)
    weight = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    max_marks = models.FloatField()

    def __str__(self):
        return self.name



