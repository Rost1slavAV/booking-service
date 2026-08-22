# 🏨 Hotel Booking Service

Сервис для управления номерами отелей и бронированиями.

## 📋 Описание проекта

Веб-приложение для управления гостиничными номерами и бронированиями.

**Основные возможности:**
- Регистрация и аутентификация пользователей
- Управление номерами отелей (создание, удаление, список с сортировкой)
- Бронирование номеров с проверкой пересечений дат
- Личный кабинет с историей бронирований
- Админ-панель для управления всеми данными

## 🛠 Технологии

- Python 3.10+
- Django 4.2+
- SQLite (по умолчанию)
- HTML + CSS + JavaScript

## 🚀 Быстрый старт

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/Rost1slavAV/booking-service.git
   cd booking-service
   
2. Создать и активировать виртуальное окружение:
    python -m venv .venv
    .venv\Scripts\activate      # Windows
    source .venv/bin/activate   # macOS / Linux

3. Установить зависимости:
    pip install -r requirements.txt

4. Применить миграции:
    python manage.py migrate

5. Создать суперпользователя:
    python manage.py createsuperuser

6. Запустить сервер:
    python manage.py runserver



🔐 Роли и права доступа
Гость — просмотр номеров, регистрация, вход

Пользователь — просмотр номеров, бронирование, отмена брони, личный кабинет

Администратор — всё, что у пользователя + управление номерами (CRUD), просмотр всех броней, удаление любых броней



🌐 API-эндпоинты

Номера (/rooms/)


POST	/rooms/api/create_room/	Создать номер (только админ)

DELETE	/rooms/api/delete/<id>/	Удалить номер (только админ)

GET	/rooms/	Список номеров с сортировкой


Бронирования (/bookings/)

POST	/bookings/create_booking/	Создать бронь

DELETE	/bookings/delete/<id>/	Удалить бронь


Пользователи (/users/)

POST	/users/register/	Регистрация

POST	/users/login/	Вход

GET	/users/logout/	Выход

GET	/users/profile/	Личный кабинет
