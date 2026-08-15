import re

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from users.models import User


def check_password(password: str) -> tuple:
    if len(password) < 8:
        return (False, 'Password must be at least 8 characters long')
    if not re.search(r'[A-Z]', password):
        return (False, 'Password must contain A-Z symbols')
    if not re.search(r'[a-z]', password):
        return (False, 'Password must contain a-z symbols')
    if not re.search(r'\d', password):
        return (False, 'The password must contain at least one digit')
    if not re.search(r'[@$!%*?&]', password):
        return (False, 'Password must contain one of @$!%*?& special symbols')
    return (True, None)


@csrf_exempt
def register(request):
    # GET-запрос → показываем форму
    if request.method == 'GET':
        return render(request, 'users/register.html')

    # POST-запрос → обрабатываем
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number', '')
        is_json = request.POST.get('format') == 'json'

        # Проверка обязательных полей
        if not username or not password or not email:
            if is_json:
                return JsonResponse({'error': 'Username, password and email are required'}, status=400)
            return render(request, 'users/register.html', {'error': 'Все поля обязательны'})

        # Проверка пароля
        is_valid, error_message = check_password(password)
        if not is_valid:
            if is_json:
                return JsonResponse({'error': error_message}, status=400)
            return render(request, 'users/register.html', {'error': error_message})

        # Проверка уникальности username
        if User.objects.filter(username=username).exists():
            if is_json:
                return JsonResponse({'error': 'Username already exists'}, status=400)
            return render(request, 'users/register.html', {'error': 'Пользователь с таким именем уже существует'})

        # Проверка уникальности email
        if User.objects.filter(email=email).exists():
            if is_json:
                return JsonResponse({'error': 'Email already exists'}, status=400)
            return render(request, 'users/register.html', {'error': 'Пользователь с таким email уже существует'})

        # Создание пользователя
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.phone_number = phone_number
            user.save()
        except Exception as e:
            if is_json:
                return render(request, 'users/register.html', {'error': f'Ошибка: {e}'})


        # Успех
        if is_json:
            return JsonResponse({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number,
                'message': 'User registered successfully'
            }, status=201)

        return render(request, 'users/register.html', {'success': 'Регистрация прошла успешно! Теперь вы можете войти.'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'users/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'users/login.html', {'error': 'Введите имя пользователя и пароль'})

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'users/login.html', {'error': 'Неверное имя пользователя или пароль'})

        login(request, user)
        return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/')