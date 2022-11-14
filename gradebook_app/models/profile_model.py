import datetime

from django import forms
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

from gradebook_app.models.common_classes import Departments, ProfileType, Grades
from gradebook_app.models.course_model import Course


class Profile(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    type = models.CharField(max_length=10, choices=ProfileType.choices())
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.CharField(max_length=100, choices=Departments.choices())
    phone = models.CharField(max_length=10, validators=[MinLengthValidator(10), RegexValidator(regex='[0-9]+', message='Phone number must be numeric')])
    date_added = models.DateField(default=datetime.date.today)
    courses = models.ManyToManyField(Course, through='ProfileCourse', related_name='profiles')

    def __str__(self):
        return self.first_name[0:7] + f" ({self.email})"


class ProfileCourse(models.Model):
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    grade = models.CharField(max_length=1, choices=Grades.choices())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'type', 'first_name', 'last_name', 'department', 'phone']


class AllocateCourseToStudentsForm(forms.Form):
    students = forms.ModelChoiceField(required=False, queryset=Profile.objects.filter(type=ProfileType.STUDENT.value).all())
    students_csv = forms.FileField(required=False)
    professors = forms.ModelChoiceField(required=False, queryset=Profile.objects.filter(type=ProfileType.PROFESSOR.value).all())
    professors_csv = forms.FileField(required=False)
