from django.apps import AppConfig


class ZolaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'zola'

    def ready(self):
        import zola.signals
