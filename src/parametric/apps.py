from django.apps import AppConfig


class ParametricConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.parametric'

    def ready(self):
        # Import signals to ensure they are registered
        import src.parametric.signals
