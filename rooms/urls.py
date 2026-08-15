from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('rooms/', views.all_rooms, name='room_list'),
    path('rooms/<int:room_id>/', views.current_room, name='pk'),
    path('rooms/api/create_room/', views.create_room, name='create_room'),
    path('rooms/api/update/<int:room_id>/', views.update_room, name='update_room'),
    path('rooms/api/delete/<int:room_id>/', views.delete_room, name='delete_room'),

    # Админ-панель
    path('rooms/admin/', views.admin_rooms, name='admin_rooms'),
    path('rooms/admin/create/', views.admin_room_create, name='admin_room_create'),
    path('rooms/admin/edit/<int:room_id>/', views.admin_room_edit, name='admin_room_edit'),
    path('rooms/admin/delete/<int:room_id>/', views.admin_room_delete, name='admin_room_delete'),
]