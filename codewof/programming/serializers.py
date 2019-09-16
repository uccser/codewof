"""Serializers for programming models."""

from rest_framework import serializers
from programming.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF questions."""

    class Meta:
        """Meta settings for serializer."""

        model = Question
        fields = (
            'slug',
            'title',
            'objects',
        )
