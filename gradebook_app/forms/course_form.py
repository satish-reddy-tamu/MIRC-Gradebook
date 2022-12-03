from django import forms

from gradebook_app.models import Course, Profile
from gradebook_app.util.enums_util import ProfileType


class AdminCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        exclude = ['thresholds']


class AllocateCourseToStudentsForm(forms.Form):
    students = forms.ModelChoiceField(required=False,
                                      queryset=Profile.objects.filter(type=ProfileType.STUDENT.value).all())
    students_csv = forms.FileField(required=False)
    professors = forms.ModelChoiceField(required=False,
                                        queryset=Profile.objects.filter(type=ProfileType.PROFESSOR.value).all())
    professors_csv = forms.FileField(required=False)
