"""Serializers for programming models."""

from rest_framework import serializers
from programming.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF users."""

    class Meta:
        """Meta settings for serializer."""

        model = User
        fields = (
            'pk',
            'email',
        )
