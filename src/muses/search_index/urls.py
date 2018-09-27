from django.conf.urls import url, include
from rest_framework_extensions.routers import ExtendedDefaultRouter
from .viewsets import (
    CollectionItemDocumentViewSet,
    CollectionItemFacetsOnlyDocumentViewSet,
)

__all__ = ('urlpatterns',)

router = ExtendedDefaultRouter()

collection_items = router.register(
    r'collectionitem',
    CollectionItemDocumentViewSet,
    base_name='collectionitem'
)

collection_items_facets_only = router.register(
    r'collectionitemfacetsonly',
    CollectionItemFacetsOnlyDocumentViewSet,
    base_name='collectionitemfacetsonly'
)

urlpatterns = [
    url(r'^', include(router.urls)),
]
