from django.apps import AppConfig


class TestproConfig(AppConfig):
    name = 'testpro'

    def ready(self):
        import testpro.signals
