from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

class AssessmentsConfig(AppConfig):
    name = 'assessments'

    def ready(self):
        import assessments.signals     