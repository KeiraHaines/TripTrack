# Import necessary Django modules
from django.apps import AppConfig

# Sets base as my app
class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
