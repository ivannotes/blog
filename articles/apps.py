from django.apps import AppConfig


class ArticleAppConfig(AppConfig):
    name = 'articles'

    def ready(self):
        from . import listeners
