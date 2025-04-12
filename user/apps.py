from django.apps import AppConfig

class UserConfig(AppConfig):  # имя уникальное
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
