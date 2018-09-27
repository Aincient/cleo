from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from six import python_2_unicode_compatible

# from muses.search_index.constants import VALUE_NOT_SPECIFIED

__all__ = (
    'AccountSettings',
    'UserCollectionItemFavourite',
    'UserSearchImage',
    'UserGroup',
)


@python_2_unicode_compatible
class UserGroup(models.Model):
    """User group."""

    name = models.CharField(
        max_length=255,
        verbose_name=_("User group"),
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='user_groups',
        verbose_name=_("Users"),
    )
    valid_from = models.DateField(
        verbose_name=_("Valid from")
    )
    valid_until = models.DateField(
        verbose_name=_("Valid until")
    )

    created = models.DateField(
        auto_now_add=True,
        verbose_name=_("Date imported"),
    )
    updated = models.DateField(
        auto_now=True,
        verbose_name=_("Date updated"),
    )

    class Meta(object):
        """Options."""

        verbose_name = _('User group')
        verbose_name_plural = _('User groups')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AccountSettings(models.Model):
    """Account settings."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name='account_settings',
        verbose_name=_("User"),
    )

    # *******************************************************************
    # ******************** Language independent data ********************
    # *******************************************************************

    language = models.CharField(
        max_length=25,
        verbose_name=_("Language"),
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
        null=True,
        blank=True
    )
    unlimited_access = models.BooleanField(
        verbose_name=_("Unlimited access"),
        default=False
    )
    num_requests = models.IntegerField(
        verbose_name=_("Number of requests"),
        default=0,
        null=True,
        blank=True
    )

    class Meta(object):
        """Options."""

        verbose_name = _('Account setting')
        verbose_name_plural = _('Account settings')

    def __str__(self):
        return _("Account settings for user {}").format(self.user.username)


@python_2_unicode_compatible
class UserCollectionItemFavourite(models.Model):
    """User collection item favourite settings."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name='user_favourites',
        verbose_name=_("User"),
    )
    collection_item = models.ForeignKey(
        'muses_collection.item',
        null=True,
        blank=True,
        related_name='collection_item_favourites',
        verbose_name=_("Collection item"),
    )

    class Meta(object):
        """Options."""

        verbose_name = _('User collection item favourite')
        verbose_name_plural = _('User collection item favourites')
        unique_together = (('user', 'collection_item'),)


@python_2_unicode_compatible
class UserSearchImage(models.Model):
    """User uploaded search image."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name='user_search_images',
        verbose_name=_("User"),
    )
    image = models.ImageField(
        upload_to='user_uploads',
        null=False,
        blank=False,
        verbose_name=_("Image"),
    )
    created = models.DateField(
        auto_now_add=True,
        verbose_name=_("Date imported"),
    )
    updated = models.DateField(
        auto_now=True,
        verbose_name=_("Date updated"),
    )

    class Meta(object):
        """Options."""

        verbose_name = _('User search image')
        verbose_name_plural = _('User search images')
