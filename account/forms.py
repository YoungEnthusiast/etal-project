from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Researcher, Collab
# from django.core.exceptions import ValidationError
# import datetime
# from django.forms.widgets import NumberInput
# from django.forms.widgets import TextInput

class CustomRegisterForm(UserCreationForm):

    # TYPE_CHOICES = [
    #     ('Researcher', 'Researcher'),
    #     ('Collaborator', 'Collaborator'),
	# 	('Admin', 'Admin'),
    #     ('SuperAdmin', 'SuperAdmin'),
    # ]
    # first_name = forms.CharField(max_length=30)
    # last_name = forms.CharField(max_length=30)

    # def clean_username(self):
    #    username = self.cleaned_data.get('username')
    #    if Researcher.objects.filter(username=username).exists():
    #        raise ValidationError("A user with the supplied email already exists")
    #    return username

    class Meta:
        model = Researcher
        # fields = ['username', 'first_name', 'last_name', 'affiliation_name', 'affiliation_address', 'city', 'state', 'country', 'password1', 'password2']
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #     self.fields['first_name'].label = 'First Name'
    #     self.fields['last_name'].label = 'Last Name'
    #     self.fields['password1'].help_text = ""
        self.fields['password2'].label = "Password Confirmation"

class CollabForm(forms.ModelForm):
    class Meta:
        model = Collab
        fields = ['title', 'abstract']
