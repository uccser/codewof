"""Serializers for programming models."""

from rest_framework import serializers
from programming.models import Question, Attempt


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF questions."""
    question_type = serializers.SerializerMethodField(read_only=True)

    def get_question_type(self, obj):
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


class AttemptSerializer(serializers.ModelSerializer):
    """Serializer for codeWOF attempts."""

    class Meta:
        """Meta settings for serializer."""

        model = Attempt
        fields = (
            'datetime',
            'pk',
            'question',
            'user_code',
            'passed_tests'
        )
