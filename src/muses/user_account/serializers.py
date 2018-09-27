from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ParseError

from .fields import Base64ImageField
from .models import UserCollectionItemFavourite, UserSearchImage

__all__ = (
    'UserCollectionItemFavouriteSerializer',
    'UserApiUsageSerializer',
    'UserSearchImageSerializer',
    'UserSearchImageFindSimilarSerializer',
)


class UserCollectionItemFavouriteSerializer(serializers.ModelSerializer):
    """UserCollectionItemFavourite serializer."""

    class Meta(object):
        """Meta options."""

        model = UserCollectionItemFavourite
        fields = (
            'url',
            'id',
            'user',
            'collection_item',
        )
        read_only_fields = ('user',)

    def create(self, validated_data):
        """Create.

        :param validated_data:
        :return:
        """
        validated_data['user'] = self.context['request'].user
        try:
            return super(UserCollectionItemFavouriteSerializer, self) \
                .create(validated_data)
        except IntegrityError as err:
            raise ParseError(
                _("You have already added that item as a favourite.")
            )


class UserApiUsageSerializer(serializers.Serializer):
    """User API usage serializer."""

    scope = serializers.CharField(required=True)
    rate = serializers.CharField(required=True)
    ident = serializers.CharField(required=True)
    num_requests_limit = serializers.IntegerField(required=True)
    duration_limit = serializers.CharField(required=True)
    current_num_requests = serializers.IntegerField(required=False)
    num_requests_left = serializers.IntegerField(required=False)

    class Meta(object):
        """Meta options."""

        fields = (
            'scope',
            'rate',
            'ident',
            'num_requests_limit',
            'duration_limit',
            'current_num_requests',
            'num_requests_left',
        )
        read_only_fields = fields[:]


class UserSearchImageSerializer(serializers.ModelSerializer):
    """UserSearchImage serializer."""

    image = Base64ImageField(required=True)

    class Meta(object):
        """Meta options."""

        model = UserSearchImage
        fields = (
            'url',
            'id',
            'user',
            'image',
            'created',
            'updated',
        )
        read_only_fields = ('user', 'created', 'updated',)

    def create(self, validated_data):
        """Create.

        :param validated_data:
        :return:
        """
        validated_data['user'] = self.context['request'].user
        try:
            return super(UserSearchImageSerializer, self) \
                .create(validated_data)
        except IntegrityError as err:
            raise ParseError(err)


class UserSearchImageFindSimilarSerializer(serializers.ModelSerializer):
    """User search image find similar serializer."""

    results = serializers.DictField()

    class Meta(object):
        """Options."""

        fields = [
            'results',
        ]
        read_only_fields = ('results',)
