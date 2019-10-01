"""Serializers for research models."""

from rest_framework import serializers
from research.models import Study, StudyGroup
from programming.serializers import QuestionWithAttemptSerializer


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

    questions = QuestionWithAttemptSerializer(many=True, read_only=True)

    class Meta:
        """Meta settings for serializer."""

        model = StudyGroup
        fields = (
            'pk',
            'title',
            'questions',
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
