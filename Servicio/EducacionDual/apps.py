from django.apps import AppConfig


class EducaciondualConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EducacionDual'

    def ready(self):
        import EducacionDual.signals
