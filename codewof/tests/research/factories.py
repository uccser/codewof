"""Module for factories for testing the POET application."""

import random
from factory import (
    DjangoModelFactory,
    Faker,
    Iterator,
    post_generation,
)
from codewof.models import Question
from research.models import (
    Study,
    StudyGroup,
)
from users.models import UserType


class StudyFactory(DjangoModelFactory):
    """Factory for generating research groups."""

    title = Faker('sentence')
    description = Faker('paragraph', nb_sentences=10)
    start_date = Faker('date_between', start_date="-2m", end_date="+1m")
    end_date = Faker('date_between', start_date="+1m", end_date="+3m")
    visible = True
    consent_form = 'MaintainingProgrammingSkills2019Form'

    class Meta:
        """Metadata for class."""

        model = Study

    @post_generation
    def add_detail(self, create, extracted, **kwargs):
        """Add detail to study."""
        # Set user types
        # 25% chance all types, otherwise one type
        if random.randint(1, 4) == 1:
            self.user_types.add(*UserType.objects.all())
        else:
            self.user_types.add(random.choice(UserType.objects.all()))


class StudyGroupFactory(DjangoModelFactory):
    """Factory for generating research study groups."""

    title = Faker('sentence')
    study = Iterator(Study.objects.all())

    class Meta:
        """Metadata for class."""

        model = StudyGroup

    @post_generation
    def add_detail(self, create, extracted, **kwargs):
        """Add groups to study."""
        question_list = list(Question.objects.all())
        self.questions.add(
            *random.sample(
                question_list,
                random.randint(1, len(question_list))
            )
        )
