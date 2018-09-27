from django.contrib.auth import get_user_model

from rest_framework import serializers

from rest_auth.serializers import UserDetailsSerializer
from rest_auth.registration.serializers import RegisterSerializer

from invitations.utils import get_invitation_model

from .models import AccountSettings

__all__ = (
    'AccountSettingsSerializer',
    'CustomUserDetailsSerializer',
    'CustomRegisterSerializer',
)

UserModel = get_user_model()


class AccountSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountSettings
        fields = ('language',)


class CustomUserDetailsSerializer(UserDetailsSerializer):
    """Custom UserDetailsSerializer."""

    account_settings = AccountSettingsSerializer()

    class Meta(object):
        """Options."""

        model = UserModel
        fields = list(UserDetailsSerializer.Meta.fields) + ['account_settings']

    def create(self, validated_data):
        """Create.

        :param validated_data:
        :return:
        """
        # Dealing with account settings separately
        account_settings_data = validated_data.pop('account_settings')

        # Standard implementation
        user = UserModel.objects.create(**validated_data)

        # Saving account settings
        account_settings = AccountSettings.objects.create(
            user=user,
            **account_settings_data
        )

        return user

    def update(self, instance, validated_data):
        """Update.

        :param instance:
        :param validated_data:
        :return:
        """
        # Deal with account settings separately
        account_settings_data = validated_data.pop('account_settings')

        # Standard implementation
        instance = super(CustomUserDetailsSerializer, self).update(
            instance,
            validated_data
        )

        # Saving account settings
        try:
            for prop, value in account_settings_data.items():
                setattr(instance.account_settings, prop, value)
            instance.account_settings.save()
        except AccountSettings.DoesNotExist as err:
            account_settings = AccountSettings.objects.create(
                user=instance,
                **account_settings_data
            )
        except Exception as err:
            pass

        return instance


class CustomRegisterSerializer(RegisterSerializer):
    """Custom registration serializer."""

    def custom_signup(self, request, user):
        try:
            Invitation = get_invitation_model()
            invitation = Invitation.objects.get(email=user.email)
            invitation.user_group.users.add(user)
        except Invitation.DoesNotExist:
            pass
