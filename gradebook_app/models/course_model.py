from django.db import models
from django import forms
from gradebook_app.models.common_classes import Departments,Semesters

class Course(models.Model):
    course_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    department = models.CharField(max_length=10, choices=Departments.choices())
    year = models.IntegerField(blank=True)
    semester = models.CharField(max_length=10, choices=Semesters.choices())
    credits = models.IntegerField(default=0)
    
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
