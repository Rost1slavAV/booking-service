from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'user', 'date_start', 'date_end')
    list_filter = ('date_start', 'date_end')