"""Models for codeWOF application."""

from random import shuffle
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from model_utils.managers import InheritanceManager
from utils.TranslatableModel import TranslatableModel

SMALL = 100
LARGE = 500
User = get_user_model()


class Profile(models.Model):
    """Profile of a user."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    points = models.IntegerField(default=0)
    goal = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)]
    )
    # earned_badges = models.ManyToManyField('Badge', through='Earned')
    # attempted_questions = models.ManyToManyField('Question', through='Attempt')

    def __str__(self):
        """Text representation of a profile."""
        return self.user.full_name()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a profile when a user is created."""
    # TODO: This can be replaced by manual creation of profile on demand
    if created:
        Profile.objects.create(user=instance, points=0)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Update a profile when a user is updated."""
    instance.profile.full_clean()
    instance.profile.save()


class LoginDay(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    day = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.day)


class Badge(models.Model):
    id_name = models.CharField(max_length=SMALL, unique=True)
    display_name = models.CharField(max_length=SMALL)
    description = models.CharField(max_length=LARGE)
    icon_name = models.CharField(null=True, max_length=SMALL)

    def __str__(self):
        return self.display_name


class Earned(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    badge = models.ForeignKey('Badge', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date)


class Token(models.Model):
    name = models.CharField(max_length=SMALL, primary_key=True)
    token = models.CharField(max_length=LARGE)

    def __str__(self):
        return self.name



class Attempt(models.Model):
    """An user attempt for a question."""

    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE
    )
    test_cases = models.ManyToManyField(
        'TestCase',
        through='TestCaseAttempt'
    )
    datetime = models.DateTimeField(auto_now_add=True)
    user_code = models.TextField()
    passed_tests = models.BooleanField(default=False)
    # skills_hinted = models.ManyToManyField('Skill', blank=True)

    def __str__(self):
        """Text representation of an attempt."""
        return "Attempted '" + str(self.question) + "' on " + str(self.datetime)


class TestCaseAttempt(models.Model):
    """An intermediate model for storing data of attempts on test cases."""

    attempt = models.ForeignKey('Attempt', on_delete=models.CASCADE)
    test_case = models.ForeignKey('TestCase', on_delete=models.CASCADE)
    passed = models.BooleanField()


# ----- Base question classes -------------------------------------------------

class Question(TranslatableModel):
    """Base class for a question for CodeWOF.

    Aims to be an abstract class as questions should be
    a particular subtype, though the class is not made
    completely abstract to allow retrieving all child
    objects through the InheritanceManager.
    """

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=SMALL)
    question_text = models.TextField()
    solution = models.TextField()
    # skill_areas = models.ManyToManyField('SkillArea', related_name='questions')
    # skills = models.ManyToManyField('Skill', blank=True)
    objects = InheritanceManager()

    def get_absolute_url(self):
        """Return URL of question on website.

        Returns:
            URL as a string.
        """
        return reverse('codewof:question', kwargs={'pk': self.pk})

    def __str__(self):
        """Text representation of a question."""
        return self.title

    # class Meta:
        # verbose_name = "Parsons Problem"
        # verbose_name_plural = "All Questions & Parsons Problems"


class TestCase(TranslatableModel):
    """Base class for a question for TestCase.

    Aims to be an abstract class as test cases should be
    a particular subtype, though the class is not made
    completely abstract to allow retrieving all child
    objects through the InheritanceManager.
    """

    number = models.PositiveSmallIntegerField(default=1)
    expected_output = models.TextField(blank=True)
    objects = InheritanceManager()


# ----- Program question ------------------------------------------------------

class QuestionTypeProgram(Question):
    """A program based question."""

    QUESTION_TYPE = 'program'

    class Meta:
        """Meta information for class."""

        verbose_name = 'Program Question'
        verbose_name_plural = 'Program Questions'


class QuestionTypeProgramTestCase(TestCase):
    """A test case for a program based question."""

    test_input = models.CharField(max_length=LARGE, blank=True)
    question = models.ForeignKey(
        QuestionTypeProgram,
        related_name='test_cases',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Meta information for class."""

        verbose_name = 'Program Question Test Case'


# ----- Function question -----------------------------------------------------

class QuestionTypeFunction(Question):
    """A function based question."""

    QUESTION_TYPE = 'function'

    class Meta:
        """Meta information for class."""

        verbose_name = 'Function Question'
        verbose_name_plural = 'Function Questions'


class QuestionTypeFunctionTestCase(TestCase):
    """A test case for a function based question."""

    test_code = models.TextField()
    question = models.ForeignKey(
        QuestionTypeFunction,
        related_name='test_cases',
        on_delete=models.CASCADE
    )

    class Meta:
        """Meta information for class."""

        verbose_name = 'Function Question Test Case'


# ----- Parsons problem question -----------------------------------------------------

class QuestionTypeParsons(Question):
    """A parson's problem question."""

    QUESTION_TYPE = 'parsons'
    lines = models.TextField()

    def lines_as_list(self):
        """Return lines as shuffled list split by newlines."""
        lines = self.lines.split('\n')
        shuffle(lines)
        return lines

    class Meta:
        """Meta information for class."""

        verbose_name = 'Parsons Problem Question'


class QuestionTypeParsonsTestCase(TestCase):
    """A test case for a parson's problem question."""

    test_code = models.TextField()
    question = models.ForeignKey(
        QuestionTypeParsons,
        related_name='test_cases',
        on_delete=models.CASCADE
    )

    class Meta:
        """Meta information for class."""

        verbose_name = 'Parsons Problem Question Test Case'


# ----- Buggy program question ------------------------------------------------

# class Buggy(Question):

#     QUESTION_TYPE = 'buggy_program'
#     buggy_program = models.TextField()

#     class Meta:
#         verbose_name = "Debugging Question (Program)"
#         verbose_name_plural = "All Debugging Questions"

# ----- Buggy function question -----------------------------------------------

# class BuggyFunction(Buggy):

#     QUESTION_TYPE = 'buggy_function'
#     function_name = models.CharField(max_length=SMALL)

#     class Meta:
#         verbose_name = "Debugging Question (Function)"
#         verbose_name_plural = "All Function Debugging Questions"

# class Skill(models.Model):
#     name = models.CharField(max_length=SMALL)
#     hint = models.CharField(max_length=LARGE)
#     subskills = models.ManyToManyField('self', symmetrical=False, blank=True)

#     def __str__(self):
#         return self.name

# class SkillArea(models.Model):
#     name = models.CharField(max_length=SMALL)

#     def __str__(self):
#         return self.name
