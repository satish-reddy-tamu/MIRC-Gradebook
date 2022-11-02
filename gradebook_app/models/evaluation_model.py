import datetime
from django.db import models
from django import forms
from gradebook_app.models.course_model import Course

class Evaluation(models.Model):
    eval_id = models.CharField(max_length=10, unique=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    eval_type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    max_score = models.IntegerField(blank=False)
    created_at = models.DateField(default=datetime.date.today)
    due_by = models.DateField(default=datetime.date.today)
    
class EvalulationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = '__all__'
