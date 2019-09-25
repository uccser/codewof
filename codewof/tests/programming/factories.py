"""Module for factories for tesing programming application."""

import random
from factory import (
    DjangoModelFactory,
    Faker,
    Iterator,
)
from programming.models import Question, Profile, Attempt


class AttemptFactory(DjangoModelFactory):
    """Factory for generating attempts."""

    profile = Iterator(Profile.objects.all())
    datetime = Faker('iso8601')
    question = Iterator(Question.objects.all())
    user_code = Faker('paragraph', nb_sentences=10)
    # True 50% of the time
    passed_tests = random.randint(1, 2) == 1



    class Meta:
        """Metadata for AttemptFactory class."""

        model = Attempt
