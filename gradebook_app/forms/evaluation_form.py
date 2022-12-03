from django import forms

from gradebook_app.models import Evaluation


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['name', 'eval_type', 'weight', 'max_marks']
