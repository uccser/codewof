"""Module for factories for testing programming application."""

import random
from factory import (
    DjangoModelFactory,
    Faker,
    Iterator,
    LazyAttribute,
    post_generation,
)
from programming.models import Question, Profile, Attempt
from django.utils import timezone


def get_random_question(obj):
    """Return a random question."""
    return random.choice(list(Question.objects.all()))


class AttemptFactory(DjangoModelFactory):
    """Factory for generating attempts."""

    profile = Iterator(Profile.objects.all())
    datetime = Faker('date_time', tzinfo=timezone.get_current_timezone())
    question = LazyAttribute(get_random_question)
    user_code = Faker('paragraph', nb_sentences=5)

    class Meta:
        """Metadata for AttemptFactory class."""

        model = Attempt

    @post_generation
    def add_detail(self, create, extracted, **kwargs):
        """Add passed_tests to Attempt."""
        # True 50% of the time
        self.passed_tests = random.randint(1, 2) == 1
