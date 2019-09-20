"""Serializers for programming models."""

from rest_framework import serializers
from research.models import Study


class StudySerializer(serializers.ModelSerializer):
    """Serializer for codeWOF studies."""

    class Meta:
        """Meta settings for serializer."""

        model = Study
        fields = (
            'pk',
            'title',
        )
