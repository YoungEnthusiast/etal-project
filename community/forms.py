from account.models import Researcher
from .models import Question, Response
from django import forms

class NewQuestionForm(forms.ModelForm):
    question_choices = [
		('Anyone', 'Anyone'),
        ('Affiliation', 'Affiliation'),
	]
    question_type = forms.ChoiceField(label="", choices=question_choices, widget=forms.RadioSelect, required = False)
    class Meta:
        model = Question
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={
                'autofocus': True,
                'placeholder': ''
            })
        }

class NewResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'You have a response to the question?'
            })
        }

class NewReplyForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'You have a reply to the response?'
            })
        }
