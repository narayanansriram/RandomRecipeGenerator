from django.contrib import admin

# Register your models here.
from .models import Room, Cuisine, Message

admin.site.register(Room)
admin.site.register(Cuisine)
admin.site.register(Message)