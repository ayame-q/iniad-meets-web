from django.apps import AppConfig


class MeetsConfig(AppConfig):
    name = 'meets'

    def ready(self):
        from . import signals
