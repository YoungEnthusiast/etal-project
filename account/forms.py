from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Researcher, Collab
# from django.core.exceptions import ValidationError
# import datetime
# from django.forms.widgets import NumberInput
# from django.forms.widgets import TextInput

class CustomRegisterForm(UserCreationForm):
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

class CustomRegisterFormResearcher(UserChangeForm):
    class Meta:
        model = Researcher
        fields = ['first_name', 'last_name', 'username', 'photograph', 'affiliation_name', 'affiliation_address', 'city', 'state', 'country']

class CollabForm(forms.ModelForm):
    collaborators_choices = [
		('Anyone', 'Anyone'),
        ('Affiliation', 'Affiliation'),
        # ('Select','Select'),
	]
    collaborators_type = forms.ChoiceField(label="", choices=collaborators_choices, widget=forms.RadioSelect, required = False)
    # collaborator = forms.ModelMultipleChoiceField(queryset=Researcher.objects.all(), label="A", widget=forms.SelectMultiple(attrs={'placeholder':'Please type a valid email address'}))
    class Meta:
        model = Collab
        fields = ['collaborators_type', 'collaborator', 'title', 'abstract', 'education', 'proposed_timeline', 'field', 'expertise_required', 'funding', 'collaborators_no', 'ownership', 'on_premises']
