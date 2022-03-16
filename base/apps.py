from django.apps import AppConfig

# Base configuration for the app
class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'