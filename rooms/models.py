from django.db import models

class Room(models.Model):
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f'Room {self.id} - {self.description}'



#return render(request, 'rooms/room_list.html', {'rooms': rooms})