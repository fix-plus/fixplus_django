from django.apps import AppConfig


class ParametricConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fixplus.parametric'

    def ready(self):
        # Import signals to ensure they are registered
        import fixplus.parametric.signals
