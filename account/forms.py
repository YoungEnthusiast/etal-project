from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Researcher, Collab, Flag, Report, Stranger, CollabDoc, CollabDoc, Task, Folder, TextUpdate
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

    photograph = forms.ImageField(widget=forms.FileInput, required=False)
    class Meta:
        model = Researcher
        fields = ['first_name', 'last_name', 'username', 'photograph', 'affiliation_name', 'about',
                    'affiliation_address', 'city', 'state', 'country', 'specialization', 'expertise',
                    'institution_name', 'institution_location', 'course', 'year', 'degree', 'award',
                    'year_join', 'position', 'award2', 'publication_number', 'patent_number', 'chapter',
                    'textbooks', 'google', 'grants', 'award3', 'gender']

class CollabForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Title'}))
    abstract = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder':'Research Description'}))
    proposed_timeline = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Proposed Timeline'}))
    field = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Research Field'}))
    expertise_required = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':"Collaborator's Expertise"}))
    collaborators_no = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':"Number of Collaborators Required"}))
    # collaborators_choices = [
	# 	('Anyone', 'Anyone'),
	# ]
    # collaborators_type = forms.ChoiceField(label="", choices=collaborators_choices, widget=forms.RadioSelect, required = False)
    # collaborators = forms.ModelChoiceField(label="", queryset=ScenarioArea.objects.distinct('scenarioAreaName'), empty_label="Placeholder")
    # collaborators = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Select'}))



    class Meta:
        model = Collab
        fields = ['title', 'funding', 'model', 'abstract', 'education', 'proposed_timeline', 'field', 'expertise_required', 'collaborators_no']
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request") # store value of request
        super().__init__(*args, **kwargs)

        self.fields['collaborators'] = forms.ModelMultipleChoiceField(queryset=Researcher.objects.filter(~Q(username=self.request.user.username)), required=False, label="My Selection")


class FlagForm(forms.ModelForm):
    reason = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Reason for flagging'}))
    class Meta:
        model = Flag
        fields = ['reason']

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(label="Due Date", widget=NumberInput(attrs={'type': 'date'}))
    class Meta:
        model = Task
        fields = ['assigned_to', 'title', 'description', 'due_date']
    def __init__(self, those0, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = those0

class StrangerForm(forms.ModelForm):
    class Meta:
        model = Stranger
        fields = ['first_username']

class CollabDocForm(forms.ModelForm):
    class Meta:
        model = CollabDoc
        fields = ['document']

class DocUpdateForm(forms.ModelForm):
    class Meta:
        model = CollabDoc
        fields = ['name']

class TaskEditForm(forms.ModelForm):
    due_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    class Meta:
        model = Task
        fields = ['assigned_to', 'title', 'status', 'description', 'due_date']

class TextUpdateForm(forms.ModelForm):
    class Meta:
        model = TextUpdate
        fields = ['text']

class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']

# queryset=Characteristics.objects.all().order_by('name'),
#                         label="Characteristics",
#                         widget=forms.CheckboxSelectMultiple)
