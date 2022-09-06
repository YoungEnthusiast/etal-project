from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Researcher, Collab, Flag, Report, Stranger, CollabDoc, CollabDoc
from django.db.models import Q
# from django.core.exceptions import ValidationError
# import datetime
# from django.forms.widgets import NumberInput
# from django.forms.widgets import TextInput
class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = Researcher
        fields = ['first_name', 'last_name', 'affiliation_name', 'password1', 'password2']
        # fields = ['affiliation_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #     self.fields['first_name'].label = 'First Name'
    #     self.fields['last_name'].label = 'Last Name'
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
        # ('Select','Select'),
	]
    collaborators_type = forms.ChoiceField(label="", choices=collaborators_choices, widget=forms.RadioSelect, required = False)
    # collaborators = forms.ModelMultipleChoiceField(queryset=Researcher.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_product_status="Unselected"))
    # collaborator = forms.ModelMultipleChoiceField(queryset=Researcher.objects.all(), label="A", widget=forms.SelectMultiple(attrs={'placeholder':'Please type a valid email address'}))
    class Meta:
        model = Collab
        fields = ['collaborators_type', 'collaborators', 'title', 'abstract', 'education', 'proposed_timeline', 'field', 'expertise_required', 'funding', 'collaborators_no', 'ownership', 'on_premises']
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request") # store value of request
        super().__init__(*args, **kwargs)

        self.fields['collaborators'] = forms.ModelMultipleChoiceField(queryset=Researcher.objects.filter(~Q(username=self.request.user.username)), required=False)


# class FirstForm(forms.ModelForm):
#     class Meta:
#         model = First
#         fields = ['session', 'subject', 'ca1', 'ca2', 'exam']
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop("request") # store value of request
#         super().__init__(*args, **kwargs)
#
#         self.fields['subject'] = forms.ModelChoiceField(queryset=Subject.objects.filter(teacher=self.request.user))
#
#
#

class FlagForm(forms.ModelForm):
    reason = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Reason for flagging'}))
    class Meta:
        model = Flag
        fields = ['reason']
# class ReportForm(forms.ModelForm):
#     reason = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':''}))
#     class Meta:
#         model = Report
#         fields = ['reason']

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
