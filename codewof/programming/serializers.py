"""Serializers for programming models."""

from rest_framework import serializers
from programming.models import Question


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
            'question_type'
        )
