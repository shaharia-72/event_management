from typing import Any
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect
from accounts import forms
from accounts.models import Organizer
from .models import Event, Participation, Participant, Category
from .forms import InterestForm, EventForm, ParticipationActionForm
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from django.core.paginator import Paginator
from django.views.generic.edit import FormView, UpdateView
from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages 

class ParticipantEventView(View):
    template_name = 'participant_event.html'

    # def get(self, request, *args, **kwargs):
        # now = timezone.now()  
    #     events = Event.objects.filter(
    #         event_registration_end__gte=now, 
    #         event_registration_start__lte=now
    #     ).order_by('event_start_date')  
        
    #     context = {
    #         'events': events
    #     }

    #     paginator = Paginator(events, 8)
    #     page_number = request.GET.get('page')
    #     page_numbers = paginator.get_page(page_number)

    #     context = {
    #         'events': page_numbers
    #     }
    #     return render(request, self.template_name, context)
    
    # def get_queryset(self):
    #     slug = self.kwargs.get('slug',None)
    #     if slug:
    #         category = get_object_or_404(Category, slug=slug)
    #         return Event.objects.filter(category=category).order_by('-event_start_date')
    #     return Event.objects.all().order_by('-event_start_date')
    
    def get(self, request, *args, **kwargs):
        # context = super().get_context_data(**kwargs)

        now = timezone.now()  
        events = Event.objects.filter(
            event_registration_end__gte=now, 
            event_registration_start__lte=now
        ).order_by('event_start_date')  
        categories = Category.objects.all()

        paginator = Paginator(events, 9)
        page_number = request.GET.get('page')
        page_numbers = paginator.get_page(page_number)

        context = {
            'events': events,
            'events': page_numbers,
            'categories': categories

        }
        
        # return context
        return render(request, self.template_name, context)

# class ParticipantEventView(ListView):
#     model = Event
#     template_name = 'participant_event.html'
#     context_object_name = 'events'
#     # paginate_by = 9

#     def get_queryset(self):
#         now = datetime.now()
#         return Event.objects.filter(event_registration_end__gte=now, event_registration_start__lte=now).order_by('event_start_date')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()
#         # now = datetime.now()

#         # events = Event.objects.filter(
#         #     event_registration_end__gte=now, 
#         #     event_registration_start__lte=now
#         # ).order_by('event_start_date')  
#         # categories = Category.objects.all()

#         # paginator = Paginator(events, 8)
#         # page_number = request.GET.get('page')
#         # page_numbers = paginator.get_page(page_number)

#         # context = {
#         #     'events': events,
#         #     'events': page_numbers,
#         #     'categories': categories

#         # }
#         return context
    
def category(request, category_id):
    now = timezone.now()
    category = Category.objects.filter(pk=category_id).first()
    
    if category is None:
        return redirect('home')
    
    events = Event.objects.filter(
        category=category,
        event_registration_end__gte=now,
        event_registration_start__lte=now
    ).order_by('event_start_date')

    paginator = Paginator(events, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    return render(request, 'participant_event.html', {
        'events': page_obj,
        'categories': categories,
        'active_category': category_id
    })

    
class ParticipantEventDetailsView(DetailView):
    model = Event
    template_name = 'participant_event_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InterestForm()
        return context

class ParticipantInterestView(FormView):
    form_class = InterestForm
    template_name = 'participant_interest.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        number_of_participants = form.cleaned_data['number_of_participants']
        
        #Participation.objects.create(participant=self.request.user.participant, event=event, number_of_participants=number_of_participants, status='pending')
        participation = Participation.objects.create(participant=self.request.user.participant, event=event, number_of_participants=number_of_participants, status='pending')
        
        participation.save()
        # return redirect('participant_event')
        return redirect(self.success_url)

    # def get_success_url(self):
    #     return redirect('participant_event')


class ParticipantHistoryView(ListView):
    model = Participation
    template_name = 'Participant_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'history'
        user = self.request.user

        # Get the user's participation history
        # Order by the event_created_at field in the Participation model
        participations = Participation.objects.filter(participant__user=user).order_by('-event_created_at')

        # Add participation details to the context
        context['participations'] = participations
        context['event_status'] = {p.event: p.status for p in participations}

        return context

# class ParticipantEventInterestView(LoginRequiredMixin,ListView):
#     model = Participant
#     template_name = 'participant_event_interest.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['active_page'] = 'my_books'
#         return context
    
#     def get_queryset(self):

#         queryset = Participant.objects.filter(user=self.request.user, status__isnull=True)
#         return queryset

# class ParticipantEventInterestView(LoginRequiredMixin,ListView):
#     model = Event
#     template_name = 'participant_event_interest.html'  
#     context_object_name = 'events' 
#     # paginate_by = 8

#     # def get(self, request, *args, **kwargs):

#     #     events = Event.objects.all
    
#     #     paginator = Paginator(events, 8)
#     #     page_number = request.GET.get('page')
#     #     page_numbers = paginator.get_page(page_number)

#     #     context = {
#     #         'events': page_numbers
#     #     }
#     #     return render(request, self.template_name, context)

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             participations = Participation.objects.filter(
#                 participant__user=user,
#                 status='confirmed'
#             )
#             return Event.objects.filter(participation__in=participations)
#         else:
#             return Event.objects.none()
#         #     return Event.objects.filter(participation__in=participations, 
#         #                                 event_registration_end__gte=now(), 
#         #                                 event_registration_start__lte=now()
#         #                                ).order_by('event_start_date')
#         # else:
#         #     return Event.objects.none()
#         # return Event.objects.filter(

#         #     paginator = Paginator(events, 8)
#         # page_number = request.GET.get('page')
#         # page_numbers = paginator.get_page(page_number)

#         # context = {
#         #     'events': page_numbers
#         # }

class ParticipantEventInterestView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'participant_event_interest.html'
    context_object_name = 'events'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            participations = Participation.objects.filter(
                participant__user=user,
                status='confirmed'
            )
            return Event.objects.filter(participation__in=participations)
        return Event.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['active_page'] = 'my_interest'
        
        # Map each event to its participation
        events = context['events']
        participation_map = {
            participation.event_id: participation
            for participation in Participation.objects.filter(participant__user=user)
        }
        
        for event in events:
            event.participation = participation_map.get(event.pk)
        
        return context


# class ParticipantPaymentConfirmView(View):
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         participation = get_object_or_404(Participation, pk=pk)
        

#         participation.status = 'confirmed'
#         participation.save()
        
#         return redirect('participant_event_interest')
# 

# class ParticipantPaymentConfirmView(View):
#      def post(self, request, *args, **kwargs):
#         participation_id = self.kwargs.get('pk')

#         try:
#             participation = Participation.objects.get(pk=participation_id, status='pending')
#             participation.status = 'confirmed'
#             participation.is_payment_confirmed = True  # Set the payment as confirmed
#             participation.save()

#             return redirect('download_invoice', pk=participation.pk)
#         except Participation.DoesNotExist:
#             return HttpResponseBadRequest("Participation not found or already confirmed")

# class ParticipantPaymentConfirmView(View):
#     template_name = 'payment_confirmed.html'  # HTML template for confirmation

#     def get(self, request, *args, **kwargs):
#         participation_id = kwargs.get('pk')
#         participation = get_object_or_404(Participation, pk=participation_id, status='pending')
        
#         # Calculate total price
#         number_of_participants = participation.number_of_participants
#         ticket_price = participation.event.event_ticket_price
#         total_cost = number_of_participants * ticket_price

#         # Prepare the context with necessary details
#         context = {
#             'event': participation.event,
#             'organizer': participation.event.organizer,
#             'ticket_price': ticket_price,
#             'number_of_participants': number_of_participants,
#             'total_cost': total_cost,
#             'participation': participation,
#         }

#         return render(request, self.template_name, context)
    

#     # def post(self, request, *args, **kwargs):
#     #     participation_id = kwargs.get('pk')

#     #     # Confirm the payment
#     #     try:
#     #         participation = Participation.objects.get(pk=participation_id, status='pending')
#     #         participation.status = 'confirmed'
#     #         participation.is_payment_confirmed = True
#     #         participation.save()

#     #         return redirect('download_invoice', pk=participation.pk)
#     #     except Participation.DoesNotExist:
#     #         return HttpResponseBadRequest("Participation not found or already confirmed")
#     def post(self, request, *args, **kwargs):
#         participation_id = kwargs.get('pk')

#         if participation_id:
#             try:
#                 participation = Participation.objects.get(pk=participation_id)

#                 # Check if the payment is already confirmed
#                 if participation.is_payment_confirmed:
#                     return HttpResponseBadRequest("Payment already confirmed")

#                 # Confirm payment
#                 participation.is_payment_confirmed = True
#                 participation.save()

#                 return redirect('download_invoice', pk=participation.pk)

#             except Participation.DoesNotExist:
#                 return HttpResponseBadRequest("Participation not found")
#         else:
#             return HttpResponseBadRequest("Invalid participation ID")

class ParticipantPaymentConfirmView(View):
    template_name = 'payment_confirmed.html'

    def get(self, request, *args, **kwargs):
        participation_id = kwargs.get('pk')
        participation = get_object_or_404(Participation, pk=participation_id, status='pending')
        
        # Calculate total price
        number_of_participants = participation.number_of_participants
        ticket_price = participation.event.event_ticket_price
        total_cost = number_of_participants * ticket_price

        # Prepare the context with necessary details
        context = {
            'event': participation.event,
            'organizer': participation.event.organizer,
            'ticket_price': ticket_price,
            'number_of_participants': number_of_participants,
            'total_cost': total_cost,
            'participation': participation,
        }

        return render(request, self.template_name, context)
 


class PaymentConfirmView(View):
       
    def post(self, request, *args, **kwargs):
        participation_id = kwargs.get('pk')

        if participation_id:
            try:
                participation = Participation.objects.get(pk=participation_id)

                # Check if the payment is already confirmed
                if participation.is_payment_confirmed:
                    return HttpResponseBadRequest("Payment already confirmed")

                # Confirm payment
                participation.is_payment_confirmed = True
                participation.save()

                return redirect('participant_event_interest')  # Adjust this URL as needed

            except Participation.DoesNotExist:
                return HttpResponseBadRequest("Participation not found")
        else:
            return HttpResponseBadRequest("Invalid participation ID")



class PaymentInvoiceDownloadView(DetailView):
    model = Participation
    template_name = 'payment_invoice_download.html'

    def get(self, request, *args, **kwargs):

        participation = self.get_object()
        if not participation.is_payment_confirmed:
            return HttpResponse("Payment not confirmed.", status=400)
        
        

        # # Prepare context for the invoice
        # context = {
        #     'event': participation.event,
        #     'participant': participation.participant,
        #     'number_of_participants': participation.number_of_participants,
        #     'organizer': participation.event.organizer,
        #     'ticket_price': participation.event.event_ticket_price,
        #     'total_member': participation.number_of_participants,
        #     'total_cost': participation.event.event_ticket_price,
        #     'transition_id': participation.transition_id
        # }
        # number_of_participants = participation.number_of_participants
        # ticket_price = participation.event.event_ticket_price
        # subtotal = number_of_participants * ticket_price
        # vat = subtotal * 0.15  # 15% VAT
        # platform_charge = subtotal * 0.05  # 5% platform charge
        # total_amount = subtotal + vat + platform_charge

        # # Prepare context for the invoice
        # context = {
        #     'event': participation.event,
        #     'participant': participation.participant,
        #     'number_of_participants': number_of_participants,
        #     'ticket_price': ticket_price,
        #     'subtotal': subtotal,
        #     'vat': vat,
        #     'platform_charge': platform_charge,
        #     'total_amount': total_amount,
        #     'transition_id': participation.transition_id,
        #     'organizer': participation.event.organizer
        # }

        if not participation.is_payment_confirmed:
            return HttpResponse("Payment not confirmed.", status=400)

        # Check for valid number_of_participants and ticket_price
        number_of_participants = participation.number_of_participants  # Default to 1 if None
        ticket_price = participation.event.event_ticket_price  # Default to 0 if None

        # Perform calculations
        subtotal = (float(number_of_participants) * float(ticket_price))
        vat = subtotal * 0.15  # 15% VAT
        platform_charge = subtotal * 0.05  # 5% platform charge
        total_amount = subtotal + vat + platform_charge

        # Prepare context for the invoice
        context = {
            'event': participation.event,
            'participant': participation.participant,
            'number_of_participants': number_of_participants,
            'ticket_price': ticket_price,
            'subtotal': subtotal,
            'vat': vat,
            'platform_charge': platform_charge,
            'total_amount': total_amount,
            'transition_id': participation.transition_id,
            'organizer': participation.event.organizer
        }

        # Render invoice as a PDF
        html_string = render_to_string('payment_invoice_download.html', context)
        pdf_file = BytesIO()
        pisa.CreatePDF(html_string.encode('UTF-8'), dest=pdf_file)

        response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{participation.transition_id}.pdf"'
        return response

class PaymentStatusView(View):
    def get(self, request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        try:
            participation = Participation.objects.get(event_id=event_id, participant=request.user.participant)
            return JsonResponse({'is_payment_confirmed': participation.is_payment_confirmed})
        except Participation.DoesNotExist:
            return JsonResponse({'is_payment_confirmed': False})
        
class OrganizerEventView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'organizer_event.html'

    def get(self, request, *args, **kwargs):
        now = timezone.now()  
        events = Event.objects.filter(

            organizer=self.request.user.organizer
        ).order_by('event_start_date')  
        categories = Category.objects.all()
        
        paginator = Paginator(events, 8)
        page_number = request.GET.get('page')
        page_numbers = paginator.get_page(page_number)

        context = {
            'events': page_numbers,
            'events': events,
            'categories': categories,
        }
        return render(request, self.template_name, context)
    
    def get_queryset(self):
        organizer= Organizer.objects.get(user=self.request.user)
        return Event.objects.filter(organizer=organizer)

class OrganizerEventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'organizer_event_creation.html'
    # success_url = 'organizer_event'

    def form_valid(self, form):
        form.instance.organizer = self.request.user.organizer
        return super().form_valid(form)
    
    def get_success_url(self):

        return reverse_lazy('or-home')
    
class OrganizerEventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'organizer_event_creation.html'


    def get_object(self, queryset = None):
        # return Event.objects.get(user = self.request.user)
        # return Event.objects.all()
        event_id = self.kwargs.get('event_id')
        return get_object_or_404(Event, id=event_id)
    
    def form_valid(self, form):
        event = form.save(commit = False)
        event.save()
        return super().form_valid(form)
    
        
    def get_success_url(self):

        return reverse_lazy('or-home')
    

class OrganizerEventParticipantsView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'participants_list.html'

    def get(self, request, *args, **kwargs):
        event = self.get_object()
        now = timezone.now()
        if event.event_registration_end >= now:
            return HttpResponse("Registration still ongoing or event has not ended.", status=400)

        participants = Participation.objects.filter(event=event, status='confirmed')
        context = {
            'event': event,
            'participants': participants,
        }

        html_string = render_to_string('participants_list.html', context)
        pdf_file = BytesIO()
        pisa.CreatePDF(html_string.encode('UTF-8'), dest=pdf_file)
        
        response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="participants_list_{event.event_id}.pdf"'
        return response

# class PDFView(View):
#     def get(self, request, *args, **kwargs):
#         event = get_object_or_404(Event, pk=kwargs['event_id'])
#         participation = Participation.objects.filter(event=event, status='confirmed')

#         context = {
#             'event': event,
#             'participation': participation,
#         }

#         html_string = render_to_string('pdf_template.html', context)
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        
#         pisa_status = pisa.CreatePDF(html_string.encode('UTF-8'), dest=response)
#         return response
    
class OrganizationHistoryView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'organization_history.html'
    context_object_name = 'organization_history'

    # def get_queryset(self):
    #     organizer = self.request.user.organizer
    #     now = datetime.now()
        
    #     events = Event.objects.filter(organizer=organizer, event_registration_end__lt=now).order_by('-event_start_date')

    #     return events
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # now = datetime.now()
        now = timezone.now()
        organizer = self.request.user.organizer
        
        events = Event.objects.filter(organizer=organizer)
        # print(f"Number of events: {events.count()}")
        context['events'] = events 
        
        event_details = []
        for event in events:
            
            # print(event.id, Participation.objects.filter(event=event).count())

            # event = Event.objects.get(id=1)

            participations = Participation.objects.filter(event=event)
            # print(f"Number of participations for event ID {event.event_id}: {participations.count()}")

            expressed_interest_count = participations.count()
            completed_payment_count = participations.filter(is_payment_confirmed=True).count()

            participant_count_sum = participations.filter(is_payment_confirmed=True).aggregate(total_participants=Sum('number_of_participants'))['total_participants'] or 0
            ticket_price_sum = participations.filter(is_payment_confirmed=True).aggregate(total_ticket_price=Sum('event__event_ticket_price'))['total_ticket_price'] or 0
            # print(f"Participant count sum: {participant_count_sum}, Ticket price sum: {ticket_price_sum}")

            # Calculate total earnings
            # total_earnings = participant_count_sum * ticket_price_sum
            total_earnings = float(ticket_price_sum)

            vat = float(total_earnings) * 0.15
            platform_charge = float(total_earnings) * 0.05
            final_earnings = ((total_earnings) - (vat + platform_charge))
            
            event_details.append({
                'event': event,
                'expressed_interest_count': expressed_interest_count,
                'completed_payment_count': completed_payment_count,
                'total_earnings': total_earnings,
                'vat': vat,
                'platform_charge': platform_charge,
                'final_earnings': final_earnings,
                'now': now,
            })
            print(f"Event details: {event_details}")
        
        context['event_details'] = event_details
        context['active_page'] = 'history'
        return context



class OrganizationDownloadView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):

        event = get_object_or_404(Event, event_id=kwargs['event_id'], organizer=self.request.user.organizer)

        participations = Participation.objects.filter(event=event, is_payment_confirmed=True)

        # context = {
        #     'event': event,  
        #     'participations': participations,
        #     'organizer': event.organizer,
        # }

        # html_string = render_to_string('participants_list_pdf.html', context)

        pdf_type = kwargs.get('pdf_type','participant_list')

        if pdf_type == 'participant_list':
            context = {
                'event': event,  
                'participations': participations,
                'organizer': event.organizer,
            }

            html_string = render_to_string('participants_list_pdf.html',context)
            filename = f'all_participants_list_of_{event.event_id}.pdf'

        elif pdf_type == 'Income_status':

            expressed_interest_count = participations.count()
            completed_payment_count = participations.filter(is_payment_confirmed=True).count()
            participant_count_sum = participations.aggregate(total_participants=Sum('number_of_participants'))['total_participants'] or 0
            ticket_price_sum = participations.aggregate(total_ticket_price=Sum('event__event_ticket_price'))['total_ticket_price'] or 0
        
            total_earnings = float(ticket_price_sum * participant_count_sum)
            vat = total_earnings * 0.15
            platform_charge = total_earnings * 0.05
            final_earnings = total_earnings - (vat + platform_charge)

            context = {
                'event': event,  
                'participations': participations,
                'organizer': event.organizer,
                'expressed_interest_count': expressed_interest_count,
                'completed_payment_count': completed_payment_count,
                'total_earnings': total_earnings,
                'vat': vat,
                'platform_charge': platform_charge,
                'final_earnings': final_earnings,
                'participant_count_sum': participant_count_sum,
            }

            html_string = render_to_string('Income_status_pdf.html',context)
            filename = f'total_Income_status_of_{event.event_id}.pdf'

        pdf_file = BytesIO()
        pdf_status = pisa.CreatePDF(html_string.encode('UTF-8'), dest=pdf_file)

        if not pdf_status.err:
            response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        else:

            return HttpResponse('Error generating PDF', status=500)
        

# class OrganizerRequestAcceptView(LoginRequiredMixin, View):
#     template_name = 'organizer_requests_accept.html'

#     def get(self, request, *args, **kwargs):
#         selected_event_id = request.GET.get('event_id')
#         events = Event.objects.filter(organizer=request.user.organizer).prefetch_related('participation_set')
#         selected_event = Event.objects.filter(event_id=selected_event_id).first() if selected_event_id else None
#         return render(request, self.template_name, {
#             'events': events,
#             'selected_event_id': selected_event_id,
#             'selected_event': selected_event
#         })

#     def post(self, request, *args, **kwargs):
#         action = request.POST.get('action')
#         participation_id = request.POST.get('participation_id')

#         try:
#             participation = Participation.objects.get(id=participation_id)
#         except Participation.DoesNotExist:
#             messages.error(request, "Participation not found.")
#             return HttpResponseRedirect(f'?event_id={request.POST.get("event_id")}')

#         if action == 'accept' and participation.status == 'pending':
#             participation.status = 'confirmed'
#             participation.is_payment_confirmed = True
#             messages.success(request, "Participation successfully confirmed.")
#         elif action == 'delete':
#             participation.delete()
#             messages.success(request, "Participation successfully deleted.")

#         participation.save()
        
#         # Redirect with event_id in query parameter
#         event_id = request.POST.get('event_id')
#         return HttpResponseRedirect(f'?event_id={event_id}')

class OrganizerRequestAcceptView(LoginRequiredMixin, ListView, FormView):
    template_name = 'organizer_requests_accept.html'
    form_class = ParticipationActionForm
    context_object_name = 'events'
    success_url = reverse_lazy('organizer_event_requests')

    def get_queryset(self):
        # Only show events with ongoing registration (registration end date is in the future)
        return Event.objects.filter(
            organizer=self.request.user.organizer, 
            event_registration_end__gte=timezone.now()
        ).prefetch_related('participation_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_event_id = self.request.GET.get('event_id')
        selected_event = None

        if selected_event_id:
            selected_event = get_object_or_404(Event, event_id=selected_event_id)

        # Create a list of forms for each 'pending' participation entry
        forms = []
        if selected_event:
            # Only show participations with 'pending' status
            for participation in selected_event.participation_set.filter(status='pending'):
                form = self.get_form(self.form_class)  # Create a form instance
                form.fields['participation_id'].initial = participation.id
                form.fields['event_id'].initial = selected_event_id
                forms.append((participation, form))  # Append tuple of participation and form

        context['forms'] = forms
        context['selected_event_id'] = selected_event_id
        context['selected_event'] = selected_event
        context['active_page'] = 'Dashboard'
        return context

    def form_valid(self, form):
        action = form.cleaned_data['action']
        participation_id = form.cleaned_data['participation_id']

        try:
            participation = Participation.objects.get(id=participation_id)
        except Participation.DoesNotExist:
            messages.error(self.request, "Participation not found.")
            return self.form_invalid(form)

        if action == 'accept' and participation.status == 'pending':
            participation.status = 'confirmed'
            participation.is_payment_confirmed = False
            messages.success(self.request, "Participation successfully confirmed.")
            participation.save()
        elif action == 'delete':
            participation.delete()
            messages.success(self.request, "Participation successfully deleted.")

        event_id = self.request.POST.get('event_id')
        return HttpResponseRedirect(f'?event_id={event_id}')
