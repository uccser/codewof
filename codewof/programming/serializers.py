"""Serializers for programming models."""

from rest_framework import serializers
from programming.models import Question, Attempt, Profile


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF questions."""

    question_type = serializers.SerializerMethodField(read_only=True)

    def get_question_type(self, obj):
        """Get question type."""
        #  TODO: avoid hitting database for every question
        # obj is model instance
        obj = Question.objects.get_subclass(pk=obj.pk)
        return obj.QUESTION_TYPE

    class Meta:
        """Meta settings for serializer."""

        model = Question
        fields = (
            'pk',
            'title',
            'question_type'
        )


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF profiles."""

    class Meta:
        """Meta settings for serializer."""

        model = Profile
        fields = (
            'user',
        )


class AttemptSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF attempts."""

    profile = ProfileSerializer()
    user_id = serializers.ReadOnlyField(source='profile.user.pk')
    user_email = serializers.ReadOnlyField(source='profile.user.email')


    class Meta:
        """Meta settings for serializer."""

        model = Attempt
        fields = (
            'datetime',
            'pk',
            'question',
            'user_code',
            'passed_tests',
            'profile',
            'user_id',
            'user_email',
        )
