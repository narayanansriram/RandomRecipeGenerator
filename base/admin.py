from django.contrib import admin

# Models for the application are registered here
from .models import Recipe, Cuisine, Message

admin.site.register(Recipe)
admin.site.register(Cuisine)
admin.site.register(Message)