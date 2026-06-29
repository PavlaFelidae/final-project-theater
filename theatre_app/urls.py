from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import (
    MakeReservationView, home_page_program, full_program, 
    send_contact_message, index_view, program_view, 
    contacts_view, reserve_view, about_view, partners_view
)

urlpatterns = [
    path('', index_view, name='index'),
    path('program-page/', program_view, name='program_page'),
    path('contacts-page/', contacts_view, name='contacts_page'),
    path('reserve-page/', reserve_view, name='reserve_page'),
    path('o-nas/', about_view, name='about_page'),
    path('partners/', partners_view, name='partners_page'),

    # API
    path('performance/<int:performance_id>/reserve/', csrf_exempt(MakeReservationView.as_view()), name='make_reservation'),
    path('program/main/', home_page_program, name='home_program'),
    path('program/all/', full_program, name='full_program'),
    path('contact/', send_contact_message, name='contact_send'),
]