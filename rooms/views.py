from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rooms.models import Room


def start_page(request):
    return render(request, 'rooms/start_page.html')


def is_admin(user):
    return user.is_authenticated and user.is_staff


def all_rooms(request):
    sort_by = request.GET.get('sort', 'price')
    order_by = request.GET.get('order', 'asc')
    file_format = request.GET.get('format', 'html')

    if sort_by not in ['price', 'created_at']:
        return JsonResponse({'error': 'Invalid sort parameter'}, status=400)

    if order_by not in ['asc', 'desc']:
        return JsonResponse({'error': 'Invalid order parameter'}, status=400)

    if sort_by == 'price':
        if order_by == 'asc':
            rooms = Room.objects.all().order_by('price')
        else:
            rooms = Room.objects.all().order_by('-price')

    elif sort_by == 'created_at':
        if order_by == 'asc':
            rooms = Room.objects.all().order_by('created_at')
        else:
            rooms = Room.objects.all().order_by('-created_at')

    if file_format == 'json':
        data = list(rooms.values('id', 'description', 'price', 'created_at'))
        return JsonResponse(data, safe=False)

    context = {
        'rooms': rooms,
        'sort_by': sort_by,
        'order_by': order_by,
    }
    return render(request, 'rooms/room_list.html', context)


def current_room(request, room_id):
    return HttpResponse(f'Вы просматриваете номер {room_id}')


def create_room(request):
    if not is_admin(request.user):
        return JsonResponse({'error': 'У вас нет прав доступа'}, status=403)

    if request.method != 'POST':
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    description = request.POST.get('description')
    price_str = request.POST.get('price')

    if not description:
        return JsonResponse({'error': 'Description is required'}, status=400)

    if not price_str:
        return JsonResponse({'error': 'Price is required'}, status=400)

    try:
        price = float(price_str)
    except ValueError:
        return JsonResponse({'error': 'Invalid price format'}, status=400)

    if price <= 0:
        return JsonResponse({'error': 'Price must be positive'}, status=400)

    room = Room.objects.create(price=price, description=description)
    return JsonResponse({'id': room.id}, status=201)


def update_room(request, room_id):
    if not is_admin(request.user):
        return JsonResponse({'error': 'У вас нет прав доступа'}, status=403)

    if request.method != 'POST':
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room does not exist'}, status=404)

    description = request.POST.get('description')
    price_str = request.POST.get('price')

    if description:
        room.description = description

    if price_str:
        try:
            room.price = float(price_str)
        except ValueError:
            return JsonResponse({'error': 'Invalid price format'}, status=400)

    room.save()
    return JsonResponse({'status': 'updated', 'id': room.id}, status=200)


def delete_room(request, room_id):
    if not is_admin(request.user):
        return JsonResponse({'error': 'У вас нет прав доступа'}, status=403)

    if request.method != 'DELETE':
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    try:
        room = Room.objects.get(id=room_id)
        room.delete()
        return JsonResponse({'status': 'deleted'}, status=200)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room does not exist'}, status=404)


# ========== АДМИН-ПАНЕЛЬ (HTML) ==========

def admin_rooms(request):
    if not is_admin(request.user):
        return redirect('/')

    rooms = Room.objects.all().order_by('price')
    return render(request, 'rooms/admin_rooms.html', {'rooms': rooms})


def admin_room_create(request):
    if not is_admin(request.user):
        return redirect('/')

    if request.method == 'POST':
        response = create_room(request)
        if response.status_code == 201:
            return redirect('/rooms/admin/')
        return render(request, 'rooms/admin_room_form.html', {'error': 'Ошибка при создании'})

    return render(request, 'rooms/admin_room_form.html')


def admin_room_edit(request, room_id):
    if not is_admin(request.user):
        return redirect('/')

    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return redirect('/rooms/admin/')

    if request.method == 'POST':
        description = request.POST.get('description')
        price_str = request.POST.get('price')

        if description:
            room.description = description

        if price_str:
            try:
                room.price = float(price_str)
            except ValueError:
                return render(request, 'rooms/admin_room_form.html', {
                    'room': room,
                    'error': 'Некорректная цена'
                })

        room.save()
        return redirect('/rooms/admin/')

    return render(request, 'rooms/admin_room_form.html', {'room': room})


def admin_room_delete(request, room_id):
    if not is_admin(request.user):
        return redirect('/')

    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return redirect('/rooms/admin/')

    if request.method == 'POST':
        delete_room(request, room_id)
        return redirect('/rooms/admin/')

    return render(request, 'rooms/admin_room_confirm_delete.html', {'room': room})