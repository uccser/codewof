"""Serializers for research models."""

from rest_framework import serializers
from research.models import Study, StudyGroup
from programming.serializers import AttemptSerializer, QuestionSerializer


class StudySerializer(serializers.ModelSerializer):
    """Serializer for codeWOF studies."""

    class Meta:
        """Meta settings for serializer."""

        model = Study
        fields = (
            'pk',
            'title',
            'user_types',
            'researchers'
        )


class StudyGroupSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF studies."""
    # gets related Questions
    groups = QuestionSerializer(many=True, read_only=True)

    class Meta:
        """Meta settings for serializer."""

        model = StudyGroup
        fields = (
            'pk',
            'title',
            'groups',
        )


class SingularStudySerializer(serializers.ModelSerializer):
    """Serializer for codeWOF studies."""
    # gets related StudyGroups
    groups = StudyGroupSerializer(many=True, read_only=True)

    class Meta:
        """Meta settings for serializer."""

        model = Study
        fields = (
            'pk',
            'title',
            'user_types',
            'researchers',
            'groups',
        )
