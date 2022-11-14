from django.db import models

from gradebook_app.models import Profile, Course, Evaluation


class Marks(models.Model):
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    eval_id = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    marks = models.FloatField(default=0)