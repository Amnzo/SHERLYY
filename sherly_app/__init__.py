# yourapp/__init__.py
default_app_config = 'sherly_app.apps.SherlyAppConfig'

from django.apps import AppConfig

default_app_config = 'yourapp.apps.YourAppConfig'

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import sherly_app.signals  # Import your signals module
