from __future__ import absolute_import, unicode_literals

import logging

from django.contrib import admin, messages
from django.conf.urls import url
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect

from .forms import AddNumRequestsForm
from .models import (
    AccountSettings,
    UserCollectionItemFavourite,
    UserGroup,
    UserSearchImage,
)


__all__ = (
    'AccountSettingsAdmin',
    'UserCollectionItemFavouriteAdmin',
    'UserSearchImageAdmin',
    'UserGroupAdmin',
)

LOGGER = logging.getLogger(__name__)


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    """UserGroup admin."""

    list_display = (
        'id',
        'name',
        'valid_from',
        'valid_until',
    )
    search_fields = (
        'id',
        'name',
    )
    filter_horizontal = (
        'users',
    )


@admin.register(AccountSettings)
class AccountSettingsAdmin(admin.ModelAdmin):
    """AccountSettings admin."""

    list_display = (
        'id',
        'get_username',
        'language',
        'unlimited_access',
        'get_num_requests',
    )
    list_filter = (
        'language',
        'unlimited_access',
    )
    search_fields = (
        'id',
        'user__id',
        'user__username',
        'user__email',
    )
    readonly_fields = (
        'num_requests',
    )

    def get_queryset(self, request):
        qs = super(AccountSettingsAdmin, self).get_queryset(request)
        qs = qs.select_related('user')
        return qs

    def get_username(self, obj):
        """Get username."""
        return "{} ({})".format(obj.user.username, obj.user.email)
    get_username.short_description = _("Username")

    def get_num_requests(self, obj):
        """Number of requests.

        :param obj:
        :return:
        """
        return """{num_requests} <a href="{url}" title="{link_title}">
                  <img src="{image_url}" alt="{image_alt}"></a>""".format(
            num_requests=obj.num_requests,
            url=reverse(
                'admin:account-add-credits',
                kwargs={'account_id': obj.id}
            ),
            link_title=_("Add credits"),
            image_url='/static/admin/img/icon-addlink.svg',
            image_alt=_("Add"),
        )
    get_num_requests.allow_tags = True
    get_num_requests.short_description = _("Num requests")

    def add_credits(self, request, account_id):
        """Add credits.

        :param request:
        :param account_id:
        :return:
        """
        account = self.get_queryset(request).get(id=account_id)
        if request.method == 'POST':
            form = AddNumRequestsForm(data=request.POST)
            if form.is_valid():
                num_request_add = form.cleaned_data['num_requests']
                account.num_requests += num_request_add
                account.save()
                messages.info(
                    request,
                    _("{} credits added").format(num_request_add)
                )
                url = reverse(
                    'admin:%s_%s_change' % (
                        account._meta.app_label,
                        account._meta.model_name
                    ),
                    args=[account.id]
                )
                return redirect(url)

        else:
            form = AddNumRequestsForm()

        context = {
            'title': _("Add num requests"),
            'object_id': account_id,
            'original': account,
            'form': form,
            'opts': account._meta,
        }
        context.update(self.admin_site.each_context(request))
        return render(
            request,
            'user_account/admin/add_credits.html',
            context
        )

    def get_urls(self):
        urls = super(AccountSettingsAdmin, self).get_urls()
        my_urls = [
            url(
                r'^(?P<account_id>\d+)/add-credits/$',
                self.add_credits,
                name='account-add-credits'
            )
        ]
        return my_urls + urls


@admin.register(UserCollectionItemFavourite)
class UserCollectionItemFavouriteAdmin(admin.ModelAdmin):
    """UserCollectionItemFavourite admin."""

    list_display = (
        'id',
        'user',
        'collection_item',
    )
    list_filter = (
        'collection_item__importer_uid',
    )
    search_fields = (
        'id',
        'user__id',
        'user__username',
        'user__email',
        'importer_uid',
    )


@admin.register(UserSearchImage)
class UserSearchImageAdmin(admin.ModelAdmin):
    """UserSearchImage admin."""

    list_display = (
        'id',
        'user',
        'image',
    )
    list_filter = (
        'user',
    )
