from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .viewsets import (
    UserCollectionItemFavouriteViewSet,
    UserApiUsageViewSet,
    UserSearchImageUploadViewSet,
    UserSearchImageFindSimilarViewSet,
)

router = DefaultRouter()

user_collection_item_favourite = router.register(
    r'usercollectionitemfavourites',
    UserCollectionItemFavouriteViewSet,
    base_name='usercollectionitemfavourite'
)

user_api_usage = router.register(
    r'userapiusage',
    UserApiUsageViewSet,
    base_name='userapiusage'
)

user_search_image = router.register(
    r'usersearchimages',
    UserSearchImageUploadViewSet,
    base_name='usersearchimage'
)

user_search_image_find_similar = router.register(
    r'usersearchimagefindsimilar',
    UserSearchImageFindSimilarViewSet,
    base_name='usersearchimagefindsimilar'
)

urlpatterns = [
    url(r'^', include(router.urls)),
]
