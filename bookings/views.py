from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rooms.models import Room
from rooms.views import is_admin
from .models import Booking

def create_booking(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to book rooms'}, status=401)

    room_id = request.POST.get('room_id')
    date_start_str = request.POST.get('date_start')
    date_end_str = request.POST.get('date_end')

    if not room_id or not date_start_str or not date_end_str:
        return JsonResponse({'error': 'Room ID, date start and date end are required'}, status=400)

    try:
        date_start = datetime.strptime(date_start_str, '%Y-%m-%d').date()
        date_end = datetime.strptime(date_end_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)

    room = get_object_or_404(Room, id=room_id)

    if date_start > date_end:
        return JsonResponse({'error': 'Start date must be before end date'}, status=400)

    if date_start < datetime.now().date():
        return JsonResponse({'error': 'Start date cannot be in the past'}, status=400)

    # Проверка пересечений
    existing_bookings = room.bookings.all()
    for booking in existing_bookings:
        if booking.date_start < date_end and booking.date_end > date_start:
            return JsonResponse({'error': 'Room is already booked for these dates'}, status=409)

    # Создание брони
    booking = Booking.objects.create(
        room=room,
        user=request.user,
        date_start=date_start,
        date_end=date_end
    )

    return JsonResponse({
        'id': booking.id,
        'message': 'Booking created successfully'
    }, status=201)


def delete_booking(request, booking_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to delete booking'}, status=401)


    booking = get_object_or_404(Booking, id=booking_id)

    if not is_admin(request.user) and booking.user != request.user:
        return JsonResponse({"error": "You don't have permission to delete this booking"}, status=403)

    booking.delete()

    return JsonResponse({'message': 'Booking deleted successfully'}, status=200)


