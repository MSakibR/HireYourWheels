from django.apps import AppConfig


class HirecarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HireCar'

    def ready(self):
        import HireCar.signals  
        
    

