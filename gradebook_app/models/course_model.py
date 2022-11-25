from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from datetime import date
from gradebook_app.models.common_classes import Departments, Semesters
from django.core.validators import MinValueValidator, MaxValueValidator


class Course(models.Model):
    course_code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    department = models.CharField(max_length=100, choices=Departments.choices())
    year = models.IntegerField(validators=[MinValueValidator(date.today().year), MaxValueValidator(date.today().year+1)])
    semester = models.CharField(max_length=10, choices=Semesters.choices())
    credits = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    max_score = models.FloatField(default=0)
    min_score = models.FloatField(default=0)
    mean_score = models.FloatField(default=0)
    thresholds = models.CharField(max_length=100, default="")


class AdminCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        exclude = ['min_score', 'max_score', 'mean_score', 'thresholds']

    def __init__(self, *args, **kwargs):
        super(AdminCourseForm, self).__init__(*args, **kwargs)
        self.fields['credits'].widget.attrs['min'] = 1
        self.fields['credits'].widget.attrs['max'] = 10
        self.fields['year'].widget.attrs['min'] = date.today().year
        self.fields['year'].widget.attrs['max'] = date.today().year + 1


