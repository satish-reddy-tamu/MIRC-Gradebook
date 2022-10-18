from enum import Enum

from django.db import models


class Departments(Enum):
    CSCE = "Computer Science and Engineering"
    ECE = "Electronics and Electrical Engineering"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def get_all_departments(cls):
        return [i.name for i in cls]


class Course(models.Model):
    course_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    department_name = models.CharField(max_length=10, choices=Departments.choices())
