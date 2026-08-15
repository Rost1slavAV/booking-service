from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('description',)