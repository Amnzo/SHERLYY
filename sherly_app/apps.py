from django.apps import AppConfig


class SherlyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sherly_app'
    def ready(self):
        # Importez et appelez la fonction pour charger les paramètres d'envoi d'e-mails
        from .models import EmailSettings
        from django.core.exceptions import ImproperlyConfigured

        try:
            email_settings = EmailSettings.objects.first()
            if email_settings:
                # Définissez les paramètres d'envoi d'e-mails dans les settings
                from django.conf import settings
                settings.EMAIL_BACKEND = email_settings.EMAIL_BACKEND
                settings.EMAIL_HOST = email_settings.EMAIL_HOST
                settings.EMAIL_HOST_USER = email_settings.EMAIL_HOST_USER
                settings.EMAIL_HOST_PASSWORD = email_settings.EMAIL_HOST_PASSWORD
                settings.EMAIL_PORT = email_settings.EMAIL_PORT
                settings.EMAIL_USE_TLS = email_settings.EMAIL_USE_TLS
                settings.DEFAULT_FROM_EMAIL = email_settings.DEFAULT_FROM_EMAIL
                settings.SERVER_EMAIL = email_settings.SERVER_EMAIL
        except ImproperlyConfigured:
            pass  # Gérez les erreurs d'accès à la base de données ou d'autres exceptions
