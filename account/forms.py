from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Researcher, Collab, Flag, Report, Stranger, CollabDoc, CollabDoc, Task
from django.db.models import Q
# from django.core.exceptions import ValidationError
# import datetime
from django.forms.widgets import NumberInput
# from django.forms.widgets import TextInput
class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = Researcher
        fields = ['first_name', 'last_name', 'affiliation_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = ""
        self.fields['password2'].label = "Password Confirmation"

class CustomRegisterFormResearcher(UserChangeForm):

    class Meta:
        model = Researcher
        fields = ['first_name', 'last_name', 'username', 'photograph', 'affiliation_name', 'affiliation_address', 'city', 'state', 'country']

class CollabForm(forms.ModelForm):
    collaborators_choices = [
		('Anyone', 'Anyone'),
        ('Affiliation', 'Affiliation'),
	]
    collaborators_type = forms.ChoiceField(label="", choices=collaborators_choices, widget=forms.RadioSelect, required = False)

    class Meta:
        model = Collab
        fields = ['collaborators_type', 'collaborators', 'title', 'abstract', 'education', 'proposed_timeline', 'field', 'expertise_required', 'funding', 'collaborators_no', 'ownership', 'on_premises']
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request") # store value of request
        super().__init__(*args, **kwargs)

        self.fields['collaborators'] = forms.ModelMultipleChoiceField(queryset=Researcher.objects.filter(~Q(username=self.request.user.username)), required=False)

class FlagForm(forms.ModelForm):
    reason = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Reason for flagging'}))
    class Meta:
        model = Flag
        fields = ['reason']

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(label="Due Date", widget=NumberInput(attrs={'type': 'date'}))
    class Meta:
        model = Task
        fields = ['assigned_to', 'title', 'description', 'due_date']

class StrangerForm(forms.ModelForm):
    class Meta:
        model = Stranger
        fields = ['first_username']

class CollabDocForm(forms.ModelForm):
    class Meta:
        model = CollabDoc
        fields = ['name', 'document']

class DocUpdateForm(forms.ModelForm):
    class Meta:
        model = CollabDoc
        fields = ['name']

class TaskEditForm(forms.ModelForm):
    due_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    class Meta:
        model = Task
        fields = ['assigned_to', 'title', 'description', 'due_date']

class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']
