from django.forms import ModelForm, DateInput
from calendarapp.models import Event, EventMember
from django import forms


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "location", "link", "reminder", "start_time", "end_time"]
        # datetime-local is a HTML5 input type
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title"}
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter location"}
            ),
            "link": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Insert Link"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Description",
                }
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control", "placeholder": "Ending time"},
                format="%Y-%m-%dT%H:%M",
            ),
            "reminder": DateInput(
                attrs={"type": "datetime-local", "class": "form-control", "placeholder": "Reminder"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)

class EventUpdateForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "start_time", "description", "location", "link", "reminder", "end_time"]
        # datetime-local is a HTML5 input type
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title"}
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter location"}
            ),
            "link": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Insert Link"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Description",
                }
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control", "placeholder": "Ending time"},
                format="%Y-%m-%dT%H:%M",
            ),
            "reminder": DateInput(
                attrs={"type": "datetime-local", "class": "form-control", "placeholder": "Reminder"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(EventUpdateForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)

class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ["user"]
