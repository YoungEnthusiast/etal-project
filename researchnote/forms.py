from django import forms
from .models import Note
from django.db.models import Q
# from django.core.exceptions import ValidationError
# import datetime
from django.forms.widgets import NumberInput
# from django.forms.widgets import TextInput

class NoteEditForm(forms.ModelForm):
    date_conducted = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    class Meta:
        model = Note
        fields = ['title', 'aims', 'date_conducted', 'location', 'setup', 'method', 'result', 'observations', 'document']
