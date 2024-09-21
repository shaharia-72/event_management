from django.urls import path
from .import views
from .views import ParticipantEventView, ParticipantEventDetailsView, ParticipantInterestView,OrganizerEventParticipantsView,ParticipantHistoryView, ParticipantEventInterestView, ParticipantPaymentConfirmView, PaymentInvoiceDownloadView, PaymentConfirmView,   OrganizerEventView, OrganizerEventCreateView, OrganizerEventUpdateView, OrganizationHistoryView,OrganizationDownloadView, OrganizerRequestAcceptView

urlpatterns = [
    # path('', ParticipantEventView.as_view(), name='participant_event'),
    path('events/<int:pk>/', ParticipantEventDetailsView.as_view(), name='event_detail'),
    path('events/<int:event_id>/interest/', ParticipantInterestView.as_view(), name='participant_interest'),
    # path('organizer/events/', OrganizerEventView.as_view(), name='organizer_event'),
    path('organizer/events/create/', OrganizerEventCreateView.as_view(), name='organizer_event_create'),
    path('organizer/events/<int:pk>/participants/', OrganizerEventParticipantsView.as_view(), name='organizer_event_participants'),
    # path('events/<int:event_id>/pdf/', PDFView.as_view(), name='event_pdf'),
    path('history/participant/', ParticipantHistoryView.as_view(), name='participant_history'),
    path('participant_event_interest/', ParticipantEventInterestView.as_view(), name='participant_event_interest'),
    path('download_invoice/<int:pk>/', PaymentInvoiceDownloadView.as_view(), name='download_invoice'),
    path('download_invoice/<int:pk>/', PaymentInvoiceDownloadView.as_view(), name='download_invoice'),
    path('payment-confirm/<int:pk>/', ParticipantPaymentConfirmView.as_view(), name='payment_confirm_view'),
    path('payment-confirmation/<int:pk>/', PaymentConfirmView.as_view(), name='payment_confirm'),
    path('organizer/event-creation', OrganizerEventCreateView.as_view(), name='event-creation'),
    path('organizer/event-update/<int:event_id>/', OrganizerEventUpdateView.as_view(), name='event-update'),
    # path('category/<slug:slug>/', CategoryEventView.as_view(), name='category_events'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('history/organizer/', OrganizationHistoryView.as_view(), name='organizer_history'),
    # path('download/<slug:event_id>/', OrganizationDownloadView.as_view(), name='organizer_history_download'),
    path('organizer/event/<slug:event_id>/pdf/<str:pdf_type>/', OrganizationDownloadView.as_view(), name='organizer_pdf'),
    # path('organizer/request-accept/', OrganizerRequestAcceptView.as_view(), name='organizer_request_accept'),
    # path('organizer/request-accept/', OrganizerRequestAcceptView.as_view(), name='organizer_request_accept'),  # without event_id
    # path('organizer/request-accept/<slug:event_id>/', OrganizerRequestAcceptView.as_view(), name='organizer_request_accept_with_event_id'),
    path('organizer/event-requests/', OrganizerRequestAcceptView.as_view(), name='organizer_request_accept'),
    
]


