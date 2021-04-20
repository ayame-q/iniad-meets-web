from django.apps import AppConfig


class MeetsConfig(AppConfig):
    name = 'meets'

    def ready(self):
        from . import signals
        from .models import Status
        try:
            Status.get_instance()
        except Status.DoesNotExist:
            Status.objects.create()
