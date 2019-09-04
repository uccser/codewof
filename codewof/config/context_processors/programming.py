"""Context processor for loading type variables for questions."""

from programming.models import (
    QuestionTypeProgram,
    QuestionTypeFunction,
    QuestionTypeParsons,
    QuestionTypeDebugging,
)


def question_types(request):
    """Return a dictionary containing question types.

    Returns:
        Dictionary containing types of questions.
    """
    return {
        "QUESTION_TYPE_PROGRAM": QuestionTypeProgram.QUESTION_TYPE,
        "QUESTION_TYPE_FUNCTION": QuestionTypeFunction.QUESTION_TYPE,
        "QUESTION_TYPE_PARSONS": QuestionTypeParsons.QUESTION_TYPE,
        "QUESTION_TYPE_DEBUGGING": QuestionTypeDebugging.QUESTION_TYPE,
    }
