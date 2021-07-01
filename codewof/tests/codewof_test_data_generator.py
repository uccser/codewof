"""Class to generate test data required for testing codewof system."""

from django.contrib.auth import get_user_model
from django.core import management
import datetime

from programming.models import (
    Question,
    Attempt,
    Achievement,
    QuestionTypeProgram,
    QuestionTypeFunction,
    QuestionTypeParsons,
    QuestionTypeDebugging,
    QuestionTypeProgramTestCase,
)

from research.models import (
    Study,
    StudyGroup,
    StudyRegistration,
)

from users.models import UserType, Group, GroupRole, Membership

User = get_user_model()


def generate_questions():
    """Generate questions for use in codeWOF tests. Questions contain minimum information and complexity."""
    Question.objects.create(slug="question-1", title='Test', question_text='Hello')

    QuestionTypeProgram.objects.create(
        slug="program-question-1",
        title='Test',
        question_text='Hello',
        solution="question_answer"
    )

    QuestionTypeFunction.objects.create(
        slug="function-question-1",
        title='Test',
        question_text='Hello',
        solution="question_answer"
    )

    QuestionTypeParsons.objects.create(
        slug="parsons-question-1",
        title='Test',
        question_text='Hello',
        solution="question_answer",
        lines="These are\nthe lines"
    )

    QuestionTypeDebugging.objects.create(
        slug="debugging-question-1",
        title='Test',
        question_text='Hello',
        solution="question_answer",
        initial_code=''
    )


def generate_users(user):
    """Generate users for codeWOF tests. Creates two basic users for unit tests."""
    management.call_command("load_user_types")
    user_john = User.objects.create_user(
        id=1,
        username='john',
        first_name='John',
        last_name='Doe',
        email='john@uclive.ac.nz',
        password='onion',
        user_type=UserType.objects.get(slug='student'),
    )
    user_john.save()

    user_sally = User.objects.create_user(
        id=2,
        username='sally',
        first_name='Sally',
        last_name='Jones',
        email='sally@uclive.ac.nz',
        password='onion',
        user_type=UserType.objects.get(slug='other'),
    )
    user_sally.save()


def generate_groups():
    """Generate groups for codeWOF tests. Groups are generated for user 1, covering all the GroupRoles."""
    group_1 = Group.objects.create(
        name='Group North',
        description='Group North is the best group.'
    )
    group_2 = Group.objects.create(
        name='Group East',
        description='Group East is the best group.'
    )
    group_3 = Group.objects.create(
        name='Group West',
        description='Group West is the best group.'
    )
    group_4 = Group.objects.create(
        name='Group South',
        description='Group South is the best group.'
    )
    group_5 = Group.objects.create(
        name='Group Mystery',
        description='Few know of this group...'
    )

    group_1.save()
    group_2.save()
    group_3.save()
    group_4.save()
    group_5.save()


def generate_memberships():
    """Generate memberships for codeWOF tests. Memberships are generated for user 1 and every group created in
    generate_groups, covering all the GroupRoles."""
    group_north = Group.objects.get(name='Group North')
    group_east = Group.objects.get(name='Group East')
    group_west = Group.objects.get(name='Group West')
    group_south = Group.objects.get(name='Group South')
    management.call_command("load_group_roles")
    user = User.objects.get(id=1)
    admin_role = GroupRole.objects.get(name='Admin')
    member_role = GroupRole.objects.get(name='Member')

    membership_1 = Membership.objects.create(
        user=user,
        group=group_north,
        role=admin_role
    )
    membership_2 = Membership.objects.create(
        user=user,
        group=group_east,
        role=member_role
    )
    membership_3 = Membership.objects.create(
        user=user,
        group=group_west,
        role=member_role
    )
    membership_4 = Membership.objects.create(
        user=user,
        group=group_south,
        role=member_role
    )

    membership_1.save()
    membership_2.save()
    membership_3.save()
    membership_4.save()


def generate_achievements():
    """Create achievements for codeWOF tests. Achievements created for each main current achievement category."""
    Achievement.objects.create(
        id_name='create-account',
        display_name='Account created',
        description='test',
        achievement_tier=0,
    )
    # Questions solved achievements
    Achievement.objects.create(
        id_name='questions-solved-100',
        display_name='Solved one hundred questions',
        description='test',
        achievement_tier=4,
    )
    Achievement.objects.create(
        id_name='questions-solved-10',
        display_name='Solved ten questions',
        description='test',
        achievement_tier=3,
        parent=Achievement.objects.get(id_name='questions-solved-100')
    )
    Achievement.objects.create(
        id_name='questions-solved-5',
        display_name='Solved five questions',
        description='test',
        achievement_tier=2,
        parent=Achievement.objects.get(id_name='questions-solved-10')
    )
    Achievement.objects.create(
        id_name='questions-solved-1',
        display_name='Solved one question',
        description='first',
        achievement_tier=1,
        parent=Achievement.objects.get(id_name='questions-solved-5')
    )
    # Attempts made achievements
    Achievement.objects.create(
        id_name='attempts-made-100',
        display_name='One hundred attempts made',
        description='test',
        achievement_tier=4,
    )
    Achievement.objects.create(
        id_name='attempts-made-10',
        display_name='Ten attempts made',
        description='test',
        achievement_tier=3,
        parent=Achievement.objects.get(id_name='attempts-made-100')
    )
    Achievement.objects.create(
        id_name='attempts-made-5',
        display_name='Five attempts made',
        description='test',
        achievement_tier=2
    )
    Achievement.objects.create(
        id_name='attempts-made-1',
        display_name='One attempt made',
        description='test',
        achievement_tier=1,
        parent=Achievement.objects.get(id_name='attempts-made-5')
    )
    # Only need one of the consecutive days achievements
    Achievement.objects.create(
        id_name='consecutive-days-2',
        display_name='Two consecutive days',
        description='test',
        achievement_tier=1,
    )


def generate_attempts():
    """
    Generate attempts for codeWOF tests.

    Attempts are generated for user 1 and question 1, with attempts created to cover consecutive days, failed attempts,
    and passed attempts. These attempts cover the main requirements to gain all test achievements.
    """
    user = User.objects.get(id=1)
    question = Question.objects.get(slug='program-question-1')
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=True)
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=False)
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=False)
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=True,
                           datetime=datetime.date(2019, 9, 9))
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=True,
                           datetime=datetime.date(2019, 9, 10))

def generate_attempts_no_defaults():
    """
    Generate attempts for codeWOF tests. Always supplies the datetime to ensure consistent testing for
    test_send_email_reminders.py
    """
    user1 = User.objects.get(id=1)
    user2 = User.objects.get(id=2)
    user3 = User.objects.get(id=3)
    question = Question.objects.get(slug='program-question-1')

    Attempt.objects.create(profile=user1.profile, question=question, passed_tests=True,
                           datetime=datetime.date(2021, 5, 20))
    Attempt.objects.create(profile=user1.profile, question=question, passed_tests=True,
                           datetime=datetime.date(2021, 5, 21))
    Attempt.objects.create(profile=user1.profile, question=question, passed_tests=True,
                           datetime=datetime.date(2021, 3, 1))

    Attempt.objects.create(profile=user2.profile, question=question, passed_tests=True,
                           datetime=datetime.date(2021, 5, 13))
    Attempt.objects.create(profile=user2.profile, question=question, passed_tests=True,
                           datetime=datetime.date(2021, 5, 13))

    Attempt.objects.create(profile=user3.profile, question=question, passed_tests=True,
                           datetime=datetime.date(2020, 5, 13))
    Attempt.objects.create(profile=user3.profile, question=question, passed_tests=True,
                           datetime=datetime.date(2021, 2, 1))


def generate_test_cases():
    """Generate test cases for codeWOF questions. Test cases are generated for program-question-1."""
    question = QuestionTypeProgram.objects.get(slug='program-question-1')

    QuestionTypeProgramTestCase.objects.create(
        id=1,
        test_input="",
        question=question
    )


def generate_study_registrations():
    """
    Generate studies, study groups and study registrations.

    One study is generated that has one study group which contains program-question-1.
    Only user 1 is registered for this study.
    """
    study = Study.objects.create(
        title='study-1',
        start_date=datetime.date(2019, 1, 15),
        end_date=datetime.date(3000, 1, 15)
    )
    question = QuestionTypeProgram.objects.get(slug='program-question-1')
    study_group = StudyGroup.objects.create(
        title='study-group-1',
        study=study,
    )
    study_group.questions.add(question)
    user = User.objects.get(id=1)
    StudyRegistration.objects.create(
        study_group=study_group,
        user=user,
    )


def generate_users_with_notifications(user):
    """Generate users for codeWOF tests with notification days set. Creates two basic users for unit tests."""
    management.call_command("load_user_types")
    user_john = User.objects.create_user(
        id=1,
        username='john',
        first_name='John',
        last_name='Doe',
        email='user1@uclive.ac.nz',
        password='onion',
        user_type=UserType.objects.get(slug='student'),
        remind_on_monday=True,
        remind_on_tuesday=False,
        remind_on_wednesday=False,
        remind_on_thursday=True,
        remind_on_friday=False,
        remind_on_saturday=False,
        remind_on_sunday=False
    )
    user_john.save()

    user_sally = User.objects.create_user(
        id=2,
        username='sally',
        first_name='Sally',
        last_name='Jones',
        email='user2@uclive.ac.nz',
        password='onion',
        user_type=UserType.objects.get(slug='other'),
        remind_on_monday=True,
        remind_on_tuesday=False,
        remind_on_wednesday=True,
        remind_on_thursday=False,
        remind_on_friday=True,
        remind_on_saturday=False,
        remind_on_sunday=False
    )
    user_sally.save()

    user_jane = User.objects.create_user(
        id=3,
        username='jane',
        first_name='Jane',
        last_name='Doe',
        email='user3@uclive.ac.nz',
        password='onion',
        user_type=UserType.objects.get(slug='other'),
        remind_on_monday=False,
        remind_on_tuesday=False,
        remind_on_wednesday=False,
        remind_on_thursday=False,
        remind_on_friday=False,
        remind_on_saturday=True,
        remind_on_sunday=False
    )
    user_jane.save()

    user_lazy = User.objects.create_user(
        id=4,
        username='lazy',
        first_name='Lazy',
        last_name='Dog',
        email='user4@uclive.ac.nz',
        password='onion',
        user_type=UserType.objects.get(slug='teacher'),
        remind_on_monday=False,
        remind_on_tuesday=False,
        remind_on_wednesday=False,
        remind_on_thursday=False,
        remind_on_friday=False,
        remind_on_saturday=False,
        remind_on_sunday=False
    )
    user_lazy.save()

    user_brown = User.objects.create_user(
        id=5,
        username='brown',
        first_name='Brown',
        last_name='Fox',
        email='user5@uclive.ac.nz',
        password='onion',
        user_type=UserType.objects.get(slug='student'),
        remind_on_monday=True,
        remind_on_tuesday=True,
        remind_on_wednesday=True,
        remind_on_thursday=True,
        remind_on_friday=True,
        remind_on_saturday=True,
        remind_on_sunday=False
    )
    user_brown.save()
