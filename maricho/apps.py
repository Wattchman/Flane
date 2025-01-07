from django.apps import AppConfig


class MarichoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maricho'

    def ready(self):
        import maricho.signals