from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Performance, Reservation, ContactMessage
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny

@method_decorator(csrf_exempt, name='dispatch')
class MakeReservationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request, performance_id):
        name = request.data.get('name')
        email = request.data.get('email')
        seats_count = request.data.get('seats_count') or request.data.get('seats')
        try:
            seats_requested = int(request.data.get('seats_count', 0))
        except ValueError:
            return Response({"error": "Некорректное количество мест"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            performance = Performance.objects.select_for_update().get(id=performance_id)

            if performance.available_seats < seats_requested:
                return Response(
                    {"error": f"Недостаточно мест. Осталось: {performance.available_seats}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            performance.available_seats -= seats_requested
            performance.save()

            reservation = Reservation.objects.create(
                performance=performance,
                customer_name=name,
                customer_email=email,
                seats_count=seats_requested
            )

        self.send_confirmation_email(reservation)

        return Response({"success": "Бронирование успешно оформлено!", "reservation_id": reservation.id}, status=status.HTTP_201_CREATED)

    def send_confirmation_email(self, reservation):
        subject = f"Билеты на спектакль: {reservation.performance.play.title}"
        message = (
            f"Уважаемый(ая) {reservation.customer_name}!\n\n"
            f"Вы успешно забронировали {reservation.seats_count} шт. билетов.\n"
            f"Спектакль: {reservation.performance.play.title}\n"
            f"Дата и время: {reservation.performance.date_time.strftime('%d.%m.%Y %H:%M')}\n"
            f"Ждем вас в театре!"
        )

        send_mail(
            subject,
            message,
            'from@theatre-prague.cz',
            [reservation.customer_email],
            fail_silently=True,
        )

@api_view(['GET'])
def home_page_program(request):
    """Алгоритм для Главной страницы: берем только 3 самых ближайших сеанса"""
    now = timezone.now()

    upcoming_performances = Performance.objects.filter(date_time__gte=now).order_by('date_time')[:3]
    
    data = []
    for p in upcoming_performances:
        data.append({
            "id": p.id,
            "play_title": p.play.title,
            "date_time": p.date_time.strftime('%d.%m.%Y %H:%M'),
            "price": float(p.ticket_price),
            "sold_out": p.is_sold_out
        })
        
    return Response(data)

@api_view(['GET'])
def full_program(request):
    """Алгоритм для страницы 'Программа': выводим вообще все будущие сеансы"""
    now = timezone.now()
    all_upcoming = Performance.objects.filter(date_time__gte=now).order_by('date_time')
    
    data = []
    for p in all_upcoming:
        data.append({
            "id": p.id,
            "play_title": p.play.title,
            "description": p.play.description,
            "date_time": p.date_time.strftime('%d.%m.%Y %H:%M'),
            "available_seats": p.available_seats,
            "price": float(p.ticket_price),
            "sold_out": p.is_sold_out
        })
        
    return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def send_contact_message(request):
    """Алгоритм обработки формы контактов"""
    name = request.data.get('name')
    email = request.data.get('email')
    subject = request.data.get('subject')
    message = request.data.get('message')
    
    if not name or not email or not message:
        return Response({"error": "Пожалуйста, заполните обязательные поля (Имя, Email, Сообщение)."}, status=400)
        
    ContactMessage.objects.create(
        name=name,
        email=email,
        subject=subject if subject else "Без темы",
        message=message
    )
    
    return Response({"success": "Ваше сообщение успешно отправлено! Администрация свяжется с вами."}, status=201)

def index_view(request):
    """Отображение главной страницы сайта"""
    return render(request, 'theatre_app/index.html')

def program_view(request):
    """Отображение страницы 'Афиша'"""
    return render(request, 'theatre_app/program.html')

def contacts_view(request):
    """Отображение страницы 'Контакты'"""
    return render(request, 'theatre_app/contacts.html')

def reserve_view(request):
    """Отображение страницы 'Бронирование'"""
    return render(request, 'theatre_app/reserve.html')

def about_view(request):
    """Отображение страницы 'О нас'"""
    return render(request, 'theatre_app/about.html')

def partners_view(request):
    """Отображение страницы 'Партнеры'"""
    return render(request, 'theatre_app/partners.html')