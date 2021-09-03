"""Serializers for research models."""

from rest_framework import serializers
from research.models import StudyRegistration


class StudyRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for research study registrations."""

    class Meta:
        """Meta settings for serializer."""

        model = StudyRegistration
        fields = (
            'pk',
            'datetime',
            'send_study_results',
            'user',
        )
