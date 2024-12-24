from django.apps import AppConfig


class JobConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fixplus.job'

    def ready(self):
        import fixplus.job.signals
