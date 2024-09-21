from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    is_participant = models.BooleanField(default=False)
    is_organizer = models.BooleanField(default=False)

    # def __str__(self):
        # return f"{self.is_participant} {self.is_organizer}"

class Participant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='participants/images/')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_interested_events(self):
        return self.events.filter(participation__status='pending')

class Organizer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)  # Adjusting for 1000 chars instead of words.
    organization_image = models.ImageField(upload_to='organizers/images/')

    def __str__(self):
        return self.organization_name

    def clean(self):
        if Organizer.objects.exclude(pk=self.pk).filter(organization_name=self.organization_name).exists():
            raise ValidationError("An organization with this name already exists.")
