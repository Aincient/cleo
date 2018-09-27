from django.conf.urls import url, include

from muses.search_index import urls as search_index_urls

urlpatterns = [
    url(r'^api/', include(search_index_urls)),
]
