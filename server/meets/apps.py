from django.apps import AppConfig
import sys


class MeetsConfig(AppConfig):
    name = 'meets'

    def ready(self):
        from . import signals
        if not "manage.py" in sys.argv or "runserver" in sys.argv:
            from .models import Status
            try:
                Status.get_instance()
            except Status.DoesNotExist:
                Status.objects.create()
