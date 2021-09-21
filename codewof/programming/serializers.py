"""Serializers for programming models."""

from rest_framework import serializers
from programming.models import Question, Attempt, Profile


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF questions."""

    question_type = serializers.SerializerMethodField(read_only=True)

    def get_question_type(self, question):
        """Get question type for the question."""
        #  TODO: avoid hitting database for every question
        question = Question.objects.get_subclass(pk=question.pk)
        return question.QUESTION_TYPE

    class Meta:
        """Meta settings for serializer."""

        model = Question
        fields = (
            'pk',
            'title',
            'question_type',
            'concepts'
        )


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF profiles."""

    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        """Meta settings for serializer."""

        model = Profile
        fields = (
            'user',
            'user_email',
        )


class AttemptSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF attempts."""

    # rename pk field so that it is clear it represents attempt id
    attempt_id = serializers.IntegerField(source='pk')
    profile = ProfileSerializer()

    class Meta:
        """Meta settings for serializer."""

        model = Attempt
        fields = (
            'attempt_id',
            'datetime',
            'question',
            'user_code',
            'passed_tests',
            'profile',
        )


class QuestionWithAttemptSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF questions."""

    # gets related attempts for questions
    attempt_set = AttemptSerializer(many=True, read_only=True)
    question_type = serializers.SerializerMethodField(read_only=True)

    def get_question_type(self, question):
        """Get question type for the question."""
        #  TODO: avoid hitting database for every question
        question = Question.objects.get_subclass(pk=question.pk)
        return question.QUESTION_TYPE

    class Meta:
        """Meta settings for serializer."""

        model = Question
        fields = (
            'pk',
            'title',
            'question_type',
            'attempt_set',
        )
