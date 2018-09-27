from django.apps import AppConfig

__all__ = ('Config',)


class Config(AppConfig):
    """Config."""

    name = 'muses.collection'
    label = 'muses_collection'
