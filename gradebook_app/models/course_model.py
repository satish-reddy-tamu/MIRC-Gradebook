from django import forms
from django.db import models
from datetime import date
from gradebook_app.models.common_classes import Departments, Semesters
from django.core.validators import MinValueValidator, MaxValueValidator


class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    department = models.CharField(max_length=100, choices=Departments.choices())
    year = models.IntegerField(validators=[MinValueValidator(date.today().year), MinValueValidator(date.today().year+1)])
    semester = models.CharField(max_length=10, choices=Semesters.choices())
    credits = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    max_score = models.FloatField(default=0)
    min_score = models.FloatField(default=0)
    mean_score = models.FloatField(default=0)
    thresholds = models.CharField(max_length=100, default="")


class AdminCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'name', 'description', 'department', 'year', 'semester', 'credits']
