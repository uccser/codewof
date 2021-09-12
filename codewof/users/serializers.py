"""Serializers for user models."""

from rest_framework import serializers
from users.models import User, UserType, Group, Membership, GroupRole, Invitation


class UserSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF users."""

    class Meta:
        """Meta settings for serializer."""

        model = User
        fields = (
            'pk',
            'email',
            'first_name',
            'last_name',
            'user_type',
            'remind_on_monday',
            'remind_on_tuesday',
            'remind_on_wednesday',
            'remind_on_thursday',
            'remind_on_friday',
            'remind_on_saturday',
            'remind_on_sunday',
            'timezone',
        )


class UserTypeSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF user types."""

    class Meta:
        """Meta settings for serializer."""

        model = UserType
        fields = (
            'pk',
            'name',
        )


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF groups."""

    class Meta:
        """Meta settings for serializer."""

        model = Group
        fields = (
            'pk',
            'name',
            'description',
            'date_created',
            'feed_enabled'
        )


class GroupRoleSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF group roles."""

    class Meta:
        """Meta settings for serializer."""

        model = GroupRole
        fields = (
            'pk',
            'name'
        )


class MembershipSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF group memberships."""
    user = serializers.StringRelatedField()
    group = serializers.StringRelatedField()
    role = serializers.StringRelatedField()

    class Meta:
        """Meta settings for serializer."""

        model = Membership
        fields = (
            'pk',
            'user',
            'group',
            'role',
            'date_joined'
        )


class InvitationSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF group invitations."""
    group = serializers.StringRelatedField()
    inviter = serializers.StringRelatedField()

    class Meta:
        """Meta settings for serializer."""

        model = Invitation
        fields = (
            'pk',
            'group',
            'inviter',
            'email',
            'date_sent',
            'date_expires'
        )
