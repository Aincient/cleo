"""
Urls.
"""

from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_auth.registration.views import ConfirmEmailView

from muses import urls as muses_urls
from muses.user_account import urls as user_account_urls
from muses.payments_subscriptions import urls as payments_subscriptions_urls

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

import views

__all__ = ('urlpatterns',)

admin.autodiscover()

urlpatterns = []

# Serving media and static in debug/developer mode.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    if settings.DEBUG_TOOLBAR is True:
        import debug_toolbar

        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

urlpatterns_args = [
    # CSRF token
    url(r'^csrftoken/', views.CSRFToken.as_view(), name='csrftoken'),

    url('^subscriptions/', include(payments_subscriptions_urls)),

    # Admin URLs
    url(r'^admin/', include(admin.site.urls)),

    # Authentication
    url(r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$',
        ConfirmEmailView.as_view(),
        name='account_confirm_email'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    # Invitations
    url(r'^invitations/',
        include('muses.invitations_addons.urls',
                namespace='invitations_addons')),
    url(r'^invitations/',
        include('invitations.urls', namespace='invitations')),

    # We do this is order to prevent Wagtail to catch all URLs when being
    # installed in root.
    # url(r'^$', views.home, name='home'),
    # url(r'^en/$', views.home, name='home', kwargs={'target_language': 'en'}),
    # url(r'^nl/$', views.home, name='home', kwargs={'target_language': 'nl'}),

    # # Home page
    url(r'^', include(muses_urls)),

    # Account
    url('^account/', include(user_account_urls)),

    # React
    url(r'^search', views.base, name='base'),

    url(r'^checkout/', views.checkout, name='checkout'),
    url(r'^mollie-webhook', views.mollie_webhook, name='mollie_webhook'),
    url(r'^order/(?P<order_id>[-\w]+)/$', views.order_redirect, name='order_redirect'),

    # Wagtail
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^pages/', include(wagtail_urls)),
]

urlpatterns += urlpatterns_args[:]
