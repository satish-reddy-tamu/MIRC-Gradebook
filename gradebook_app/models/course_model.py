from datetime import date

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from gradebook_app.util.enums_util import Departments, Semesters


class Course(models.Model):
    course_code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    department = models.CharField(max_length=100, choices=Departments.choices())
    year = models.IntegerField(
        validators=[MinValueValidator(date.today().year), MaxValueValidator(date.today().year + 1)])
    semester = models.CharField(max_length=10, choices=Semesters.choices())
    credits = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    thresholds = models.CharField(max_length=100, default="")



