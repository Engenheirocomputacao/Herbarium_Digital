from django.apps import AppConfig



class FitoterapicoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fitoterapico'

    def ready(self):
        import fitoterapico.signals
