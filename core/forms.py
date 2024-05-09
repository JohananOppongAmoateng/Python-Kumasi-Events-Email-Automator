from django import forms

from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description','location']


class UploadCSVFileForm(forms.Form):
    csv_file = forms.FileField()