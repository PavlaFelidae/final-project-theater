from django.db import models
from django.core.validators import MinValueValidator

class Play(models.Model):
    """Модель спектакля (описание, медиа)"""
    title = models.CharField(max_length=200, verbose_name="Название спектакля")
    description = models.TextField(verbose_name="Описание")
    duration_minutes = models.PositiveIntegerField(verbose_name="Длительность (мин)")
    image = models.ImageField(upload_to='plays/', verbose_name="Афиша", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Отображать на сайте")

    def __str__(self):
        return self.title

class Performance(models.Model):
    """Модель конкретного сеанса (дата, время, билеты)"""
    play = models.ForeignKey(Play, on_delete=models.CASCADE, related_name='performances', verbose_name="Спектакль")
    date_time = models.DateTimeField(verbose_name="Дата и время начала")
    total_seats = models.PositiveIntegerField(verbose_name="Всего мест в зале")
    available_seats = models.PositiveIntegerField(verbose_name="Доступно мест")
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена билета (CZK)")

    @property
    def is_sold_out(self):
        return self.available_seats <= 0

    def __str__(self):
        return f"{self.play.title} - {self.date_time.strftime('%d.%m.%Y %H:%M')}"

class Reservation(models.Model):
    """Модель резервации билетов"""
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name='reservations', verbose_name="Сеанс")
    customer_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    customer_email = models.EmailField(verbose_name="Email")
    seats_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], 
        verbose_name="Количество билетов"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронирования")

    def __str__(self):
        return f"Бронь #{self.id} на {self.performance.play.title}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя отправителя")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Тема сообщения")
    message = models.TextField(verbose_name="Текст сообщения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def __str__(self):
        return f"Сообщение от {self.name} — {self.subject}"