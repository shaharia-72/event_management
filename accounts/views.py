# from django.shortcuts import render, redirect
# from django.urls import reverse_lazy
# from django.contrib.auth.views import LoginView, LogoutView
# from django.contrib.auth import logout
# # from django.contrib.sites.shortcuts import get_current_site
# # from django.template.loader import render_to_string
# # from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# # from django.utils.encoding import force_bytes, force_text
# # from django.contrib.auth.tokens import default_token_generator
# # from django.core.mail import send_mail
# from django.contrib.auth import get_user_model
# from django.views.generic import CreateView
# from .forms import ParticipantRegistrationForm, OrganizerRegistrationForm
# from .models import Participant, Organizer
# # Create your views here.


# User = get_user_model()

# class ParticipantRegistrationView(CreateView):
#     model = User
#     form_class = ParticipantRegistrationForm
#     template_name = 'participant_register.html'
#     success_url = reverse_lazy('login')

#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.is_participant = True
#         user.save()
#         Participant.objects.create(user=user)
#         # self.send_confirmation_email(user)
#         return redirect('home')

#     # def send_confirmation_email(self, user):
#     #     current_site = get_current_site(self.request)
#     #     subject = 'Activate Your Account'
#     #     message = render_to_string('email_confirmation.html', {
#     #         'user': user,
#     #         'domain': current_site.domain,
#     #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#     #         'token': default_token_generator.make_token(user),
#     #     })
#     #     send_mail(subject, message, 'noreply@example.com', [user.email])

# class OrganizerRegistrationView(CreateView):
#     model = User
#     form_class = OrganizerRegistrationForm
#     template_name = 'organizer_register.html'
#     success_url = reverse_lazy('login')

#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.is_organizer = True
#         user.save()
#         Organizer.objects.create(user=user)
#         # self.send_confirmation_email(user)
#         return redirect('home')

#     # def send_confirmation_email(self, user):
#     #     current_site = get_current_site(self.request)
#     #     subject = 'Activate Your Account'
#     #     message = render_to_string('email_confirmation.html', {
#     #         'user': user,
#     #         'domain': current_site.domain,
#     #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#     #         'token': default_token_generator.make_token(user),
#     #     })
#     #     send_mail(subject, message, 'noreply@example.com', [user.email])

# # class EmailVerificationView(View):
# #     def get(self, request, uidb64, token):
# #         try:
# #             uid = force_text(urlsafe_base64_decode(uidb64))
# #             user = User.objects.get(pk=uid)
# #         except(TypeError, ValueError, OverflowError, User.DoesNotExist):
# #             user = None

# #         if user is not None and default_token_generator.check_token(user, token):
# #             user.is_active = True
# #             user.save()
# #             return redirect('login')
# #         else:
# #             return render(request, 'activation_invalid.html')


from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import ParticipantRegistrationForm, OrganizerRegistrationForm, ParticipantProfileUpdateForm, OrganizerProfileUpdateForm
from .models import CustomUser, Participant, Organizer
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import TemplateView


class ParticipantRegistrationView(FormView):
    template_name = 'register.html'
    form_class = ParticipantRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_participant = True  # Ensure the user is marked as a participant
        user.save()
        Participant.objects.create(
            user=user,
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            profile_image=form.cleaned_data.get('profile_image')  # Optional
        )
        login(self.request, user)
        return super().form_valid(form)


class OrganizerRegistrationView(FormView):
    template_name = 'register.html'
    form_class = OrganizerRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_organizer = True  # Ensure the user is marked as an organizer
        user.save()
        Organizer.objects.create(
            user=user,
            organization_name=form.cleaned_data['organization_name'],
            location=form.cleaned_data['location'],
            description=form.cleaned_data['description'],
            organization_image=form.cleaned_data.get('organization_image')  # Optional
        )
        login(self.request, user)
        return super().form_valid(form)


class RegisterView(TemplateView):
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['participant_form'] = ParticipantRegistrationForm()
        context['organizer_form'] = OrganizerRegistrationForm()
        return context


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):

        user = self.request.user
        if user.is_organizer:
            return reverse_lazy('or-home')
        elif user.is_participant:
            return reverse_lazy('home')
        else:
            return reverse_lazy('lo-home')


@login_required
def logout_view(request):
    logout(request)
    return redirect('lo-home')

class ParticipantProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'participant_profile.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participant = Participant.objects.get(user=self.request.user)
        context['profile'] = participant
        context['active_page'] = 'profile'

        return context


class OrganizerProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'organizer_profile.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organizer = Organizer.objects.get(user=self.request.user)
        context['profile'] = organizer
        context['active_page'] = 'profile'
        return context


class ParticipantProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = Participant
    form_class = ParticipantProfileUpdateForm
    template_name = 'update_participant_profile.html'
    # success_url = ('participant_profile')

    def get_object(self, queryset=None):
        # return self.request.user
        return Participant.objects.get(user = self.request.user)
    
    def form_valid(self, form):
        # user = form.save(commit=False)
        # user.save()
        participant = form.save(commit=False)
        participant.user.save()
        participant.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('participant_profile')
    
class OrganizerProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = Organizer
    form_class = OrganizerProfileUpdateForm
    template_name = 'update_organizer_profile.html'
    # success_url = ('organizer_profile')

    def get_object(self, queryset=None):
        # return self.request.user
        return Organizer.objects.get(user = self.request.user)


    def form_valid(self, form):
        # user = form.save(commit=False)
        # user.save()
        organizer = form.save(commit=False)
        organizer.user.email = form.cleaned_data['email']
        # organizer.user = self.request.user
        organizer.user.save()
        # organizer.user.save()
        organizer.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('organizer_profile')
