from django import forms

from gradebook_app.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'type', 'first_name', 'last_name', 'department', 'phone']
