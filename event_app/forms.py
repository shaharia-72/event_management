from django import forms
from .models import Event, Participant

class InterestForm(forms.Form):
    number_of_participants = forms.IntegerField(min_value=1, label="Number of participants")

class EventForm(forms.ModelForm):

    event_registration_start = forms.DateTimeField( 
        widget=forms.DateInput(
                attrs={
                'class': 'form-control',
                'type': 'datetime-local'
                }
            )
    )
    event_registration_end = forms.DateTimeField( 
        widget=forms.DateInput(
                attrs={
                'class': 'form-control',
                'type': 'datetime-local'
                }
            )
    )
    event_start_date = forms.DateTimeField( 
        widget=forms.DateInput(
                attrs={
                'class': 'form-control',
                'type': 'datetime-local'
                }
            )
    )

    class Meta:
        model = Event
        fields = ['event_id','event_title', 'event_description', 'event_location', 'event_image', 'event_ticket_price', 'event_registration_start', 'event_registration_end', 'event_start_date', 'event_max_participants', 'category',]


class ParticipationActionForm(forms.Form):
    participation_id = forms.IntegerField(widget=forms.HiddenInput())
    action = forms.ChoiceField(choices=[('accept', 'Accept'), ('delete', 'Delete')])
    event_id = forms.CharField(widget=forms.HiddenInput())  # To keep track of the event