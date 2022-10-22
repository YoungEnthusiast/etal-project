from django import forms
from .models import Note
from django.db.models import Q
# from django.core.exceptions import ValidationError
# import datetime
from django.forms.widgets import NumberInput, DateInput
# from django.forms.widgets import TextInput

class NoteEditForm(forms.ModelForm):
    date_conducted = forms.DateTimeField(widget=NumberInput(attrs={'type': 'date'}))
    class Meta:
        model = Note
        fields = ['title', 'aims', 'date_conducted', 'location', 'setup', 'method', 'result', 'observations', 'document']

class NoteForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Title'}))
    aims = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Aims'}))
    location = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Location'}))
    setup = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Setup'}))
    method = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Method'}))
    result = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Result'}))
    observations = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Observations'}))

    date_conducted = forms.DateTimeField(widget=DateInput(attrs={"type": "datetime-local",}, format="%Y-%m-%dT%H:%M",))
    class Meta:
        model = Note
        fields = ['title', 'aims', 'date_conducted', 'location', 'setup', 'method', 'result', 'observations', 'document']
