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

class CustomRegisterFormQwikCust(UserChangeForm):
    GENDER_CHOICES = [
		('Male','Male'),
		('Female', 'Female')
	]
    TYPE_CHOICES = [
        ('QwikCustomer', 'QwikCustomer'),
		('QwikVendor', 'QwikVendor'),
        ('QwikPartner', 'QwikPartner'),
        ('QwikA', 'QwikA'),
    ]
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, widget=forms.RadioSelect, required=False)
    dob = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), required=False, label="Date of Start of Business")
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=False)
    username = forms.CharField(max_length=20)
    # def clean_email(self):
    #    email = self.cleaned_data.get('email')
    #    if Person.objects.filter(email=email).exists():
    #        raise ValidationError("A user with the supplied email already exists")
    #    return email

    def clean_dob(self):
        try:
            dob = self.cleaned_data.get('dob')
            if dob > datetime.date.today():
                raise ValidationError("The selected date is invalid. Please re-select another")
            return dob
        except:
            pass


    def __init__(self, *args, **kwargs):
        super(CustomRegisterFormQwikCust, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['username'].required = False
            self.fields['username'].widget.attrs['disabled'] = 'disabled'
            self.fields['first_name'].required = False
            self.fields['first_name'].widget.attrs['disabled'] = 'disabled'
            self.fields['last_name'].required = False
            self.fields['last_name'].widget.attrs['disabled'] = 'disabled'
            self.fields['holding'].required = False
            self.fields['holding'].widget.attrs['disabled'] = 'disabled'
            self.fields['referrer'].required = False
            self.fields['referrer'].widget.attrs['disabled'] = 'disabled'
            self.fields['first_name'].label = 'First Name'
            self.fields['last_name'].label = 'Last Name'
            self.fields['email'].help_text = "This field must be a valid email address"
            self.fields['phone_number'].label = "Phone Number"


    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.username
        else:
            return self.cleaned_data.get('username', None)

    def clean_first_name(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.first_name
        else:
            return self.cleaned_data.get('first_name', None)

    def clean_last_name(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.last_name
        else:
            return self.cleaned_data.get('last_name', None)

    def clean_holding(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.holding
        else:
            return self.cleaned_data.get('holding', None)

    def clean_referrer(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.referrer
        else:
            return self.cleaned_data.get('referrer', None)

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'username', 'holding', 'com_name', 'dob', 'phone_number', 'gender', 'state', 'city', 'lg', 'outlet', 'about_me', 'address', 'referrer', 'photograph']


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
