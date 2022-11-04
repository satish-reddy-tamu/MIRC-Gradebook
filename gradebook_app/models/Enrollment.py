from django import forms
from django.db import models

from gradebook_app.models.course_model import Course
from gradebook_app.models.profile_model import Profile


class Enrollment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) 
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class EnrollmentForm(forms.Form):
    student_email = forms.CharField(required=False)
    file = forms.FileField(required=False)