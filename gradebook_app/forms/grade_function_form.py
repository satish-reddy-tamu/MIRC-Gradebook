from django import forms
from django.core.exceptions import ValidationError


class GradeFunctionForm(forms.Form):
    A = forms.IntegerField(min_value=0, max_value=100)
    B = forms.IntegerField(min_value=0, max_value=100)
    C = forms.IntegerField(min_value=0, max_value=100)
    D = forms.IntegerField(min_value=0, max_value=100)
    E = forms.IntegerField(min_value=0, max_value=100)
    F = forms.IntegerField(min_value=0, max_value=100)

    def clean(self):
        values = list(self.cleaned_data.values())
        if values != sorted(values, reverse=True):
            raise ValidationError("Given Values are not sorted")
