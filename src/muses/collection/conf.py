import os

from django.conf import settings


__all__ = (
    'COLLECTION_IMAGES_BASE_PATH',
    'COLLECTION_IMAGES_BASE_URL',
    'COLLECTION_IMAGES_SOURCE_DIR_FOR_INDEX',
    'PLEIADES_PATH',
)


COLLECTION_IMAGES_BASE_PATH = getattr(
    settings,
    'COLLECTION_IMAGES_BASE_PATH',
    os.path.join(settings.MEDIA_ROOT, 'collection_images')
)

COLLECTION_IMAGES_BASE_URL = getattr(
    settings,
    'COLLECTION_IMAGES_BASE_URL',
    os.path.join(settings.MEDIA_URL, 'collection_images')
)

COLLECTION_IMAGES_SOURCE_DIR_FOR_INDEX = getattr(
    settings,
    'COLLECTION_IMAGES_SOURCE_DIR_FOR_INDEX',
    os.path.join(settings.MEDIA_URL, 'collection_images_medium')
)

PLEIADES_PATH = getattr(
    settings,
    'PLEIADES_PATH',
    os.path.join(os.path.dirname(settings.BASE_DIR), 'initial', 'pleiades', 'pleiades.json')
)