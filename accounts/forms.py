from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Participant, Organizer

class ParticipantRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'profile_image']

class OrganizerRegistrationForm(UserCreationForm):
    organization_name = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea, max_length=1000)
    organization_image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username','organization_name', 'email','location', 'password1', 'password2', 'description', 'organization_image']


class ParticipantProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'email', 'profile_image']


class OrganizerProfileUpdateForm(forms.ModelForm):
    organization_name = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea, max_length=1000)
    organization_image = forms.ImageField(required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Organizer
        fields = ['email', 'organization_name', 'location', 'description', 'organization_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].initial = self.instance.user.email

