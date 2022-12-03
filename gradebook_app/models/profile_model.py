import datetime


from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

from gradebook_app.models.course_model import Course
from gradebook_app.util.enums_util import Departments, ProfileType, Grades


class Profile(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    type = models.CharField(max_length=10, choices=ProfileType.choices())
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.CharField(max_length=100, choices=Departments.choices())
    phone = models.CharField(max_length=10,
                             validators=[MinLengthValidator(10),
                                         RegexValidator(regex='[0-9]+',
                                                        message='Phone number must be numeric')])
    date_added = models.DateField(default=datetime.date.today)
    courses = models.ManyToManyField(Course, through='ProfileCourse', related_name='profiles')

    def __str__(self):
        return self.first_name[0:7] + f" ({self.email})"


class ProfileCourse(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    grade = models.CharField(max_length=1, choices=Grades.choices())
