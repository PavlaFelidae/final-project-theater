from django.contrib import admin
from .models import Play, Performance, Reservation, ContactMessage

@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration_minutes', 'is_active')
    search_fields = ('title',)

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('play', 'date_time', 'available_seats', 'total_seats', 'is_sold_out_status')
    list_filter = ('date_time', 'play')

    def is_sold_out_status(self, obj):
        return "Солд-аут ❌" if obj.is_sold_out else f"Свободно: {obj.available_seats} 🎟️"
    is_sold_out_status.short_description = "Статус билетов"

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'performance', 'customer_name', 'seats_count', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('customer_name', 'customer_email')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    search_fields = ('name', 'email', 'subject')