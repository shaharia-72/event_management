# urls.py
from django.urls import path
from .views import RegisterView, ParticipantRegistrationView, OrganizerRegistrationView, CustomLoginView,logout_view,ParticipantProfileView, OrganizerProfileView, ParticipantProfileUpdateView, OrganizerProfileUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register/participant/', ParticipantRegistrationView.as_view(), name='register_participant'),
    path('register/organizer/', OrganizerRegistrationView.as_view(), name='register_organizer'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('participant/profile/', ParticipantProfileView.as_view(), name='participant_profile'),
    path('organizer/profile/', OrganizerProfileView.as_view(), name='organizer_profile'),
    path('participant/profile/update/', ParticipantProfileUpdateView.as_view(), name='update_participant_profile'),
    path('organizer/profile/update/', OrganizerProfileUpdateView.as_view(), name='update_organizer_profile'),
]
