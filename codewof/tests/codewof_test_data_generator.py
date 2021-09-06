"""Class to generate test data required for testing codewof system."""

from django.contrib.auth import get_user_model
from allauth.account.admin import EmailAddress
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
    Like
)
from research.models import StudyRegistration
from users.models import UserType, Group, GroupRole, Membership, Invitation

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
    """Generate users for codeWOF tests. Creates multiple basic users for unit tests."""
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

    user_alex = User.objects.create_user(
        id=3,
        username='alex',
        first_name='Alex',
        last_name='Atkinson',
        email='alex@uclive.ac.nz',
        password='onion',
        user_type=UserType.objects.get(slug='teacher'),
    )
    user_alex.save()

    user_jane = User.objects.create_user(
        id=4,
        username='jane',
        first_name='Jane',
        last_name='Doe',
        email='jane@uclive.ac.nz',
        password='onion',
        user_type=UserType.objects.get(slug='student'),
    )
    user_jane.save()


def generate_groups():
    """Generate groups for codeWOF tests. Groups are generated for user 1, covering all the GroupRoles."""
    group_1 = Group.objects.create(
        name='Group North',
        description='Group North is the best group.',
        feed_enabled=True
    )
    group_2 = Group.objects.create(
        name='Group East',
        description='Group East is the best group.',
        feed_enabled=False
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
    group_6 = Group.objects.create(
        name='Team 300',
        description='Rite of Passage'
    )
    group_7 = Group.objects.create(
        name='Team CSERG',
        description='We made CodeWOF.'
    )
    group_8 = Group.objects.create(
        name='Class 1',
        description='The Group for Class 1.'
    )

    group_1.save()
    group_2.save()
    group_3.save()
    group_4.save()
    group_5.save()
    group_6.save()
    group_7.save()
    group_8.save()


def generate_memberships():
    """Generate memberships for codeWOF tests, covering all the GroupRoles."""
    group_north = Group.objects.get(name='Group North')
    group_east = Group.objects.get(name='Group East')
    group_west = Group.objects.get(name='Group West')
    group_south = Group.objects.get(name='Group South')
    management.call_command("load_group_roles")
    user1 = User.objects.get(id=1)
    user2 = User.objects.get(id=2)
    user3 = User.objects.get(id=3)
    admin_role = GroupRole.objects.get(name='Admin')
    member_role = GroupRole.objects.get(name='Member')

    membership_1 = Membership.objects.create(
        user=user1,
        group=group_north,
        role=admin_role
    )
    membership_2 = Membership.objects.create(
        user=user1,
        group=group_east,
        role=member_role
    )
    membership_3 = Membership.objects.create(
        user=user1,
        group=group_west,
        role=member_role
    )
    membership_4 = Membership.objects.create(
        user=user1,
        group=group_south,
        role=member_role
    )
    membership_5 = Membership.objects.create(
        user=user2,
        group=group_north,
        role=member_role
    )
    membership_6 = Membership.objects.create(
        user=user3,
        group=group_north,
        role=member_role
    )

    membership_1.save()
    membership_2.save()
    membership_3.save()
    membership_4.save()
    membership_5.save()
    membership_6.save()


def generate_email_accounts():
    """Generate email accounts for user 1 and 2 for codeWOF tests."""
    user1 = User.objects.get(id=1)
    user2 = User.objects.get(id=2)
    email1 = EmailAddress(
        user=user1,
        email=user1.email,
        primary=True,
        verified=True
    )
    email2 = EmailAddress(
        user=user1,
        email="john@mail.com",
        primary=False,
        verified=True
    )
    email3 = EmailAddress(
        user=user1,
        email="jack@mail.com",
        primary=False,
        verified=False
    )
    email4 = EmailAddress(
        user=user2,
        email=user2.email,
        primary=True,
        verified=True
    )
    email1.save()
    email2.save()
    email3.save()
    email4.save()


def generate_invitations():
    """Generate invitations for codeWOF tests."""
    group_team_300 = Group.objects.get(name='Team 300')
    group_team_cserg = Group.objects.get(name='Team CSERG')
    group_mystery = Group.objects.get(name='Group Mystery')
    user1 = User.objects.get(id=1)
    user2 = User.objects.get(id=2)

    invitation_1 = Invitation.objects.create(
        email=user1.email,
        group=group_team_300,
        inviter=user2,
        date_sent=datetime.date(2020, 10, 21),
        date_expires=datetime.date(2021, 10, 21)
    )
    invitation_2 = Invitation.objects.create(
        email="john@mail.com",
        group=group_mystery,
        inviter=user2,
        date_sent=datetime.date(2020, 10, 22),
        date_expires=datetime.date(2021, 10, 22)
    )
    invitation_3 = Invitation.objects.create(
        email=user1.email,
        group=group_team_cserg,
        inviter=user2,
        date_sent=datetime.date(2020, 10, 20),
        date_expires=datetime.date(2020, 10, 20)
    )

    invitation_1.save()
    invitation_2.save()
    invitation_3.save()


def generate_invalid_invitations():
    """Generate invalid invitations for codeWOF tests."""
    group_north = Group.objects.get(name='Group North')
    group_mystery = Group.objects.get(name='Group Mystery')
    group_class_1 = Group.objects.get(name='Class 1')
    user1 = User.objects.get(id=1)
    user2 = User.objects.get(id=2)

    # Duplicate
    invitation_1 = Invitation.objects.create(
        email=user1.email,
        group=group_mystery,
        inviter=user2,
        date_sent=datetime.date(2020, 10, 21)
    )
    # Unverified email
    invitation_2 = Invitation.objects.create(
        email="jack@mail.com",
        group=group_class_1,
        inviter=user2,
        date_sent=datetime.date(2020, 10, 22)
    )
    # Already a member
    invitation_3 = Invitation.objects.create(
        email=user1.email,
        group=group_north,
        inviter=user2,
        date_sent=datetime.date(2020, 10, 20)
    )

    invitation_1.save()
    invitation_2.save()
    invitation_3.save()


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


def generate_likes():
    """Generate likes for codeWOF tests."""
    sally = User.objects.get(id=2)
    alex = User.objects.get(id=3)
    jane = User.objects.get(id=4)
    attempt = Attempt.objects.first()
    Like.objects.create(attempt=attempt, user=sally)
    Like.objects.create(attempt=attempt, user=alex)
    Like.objects.create(attempt=attempt, user=jane)


def generate_feed_attempts():
    """
    Generate attempts for codeWOF tests.

    Attempts are generated for users 1 to 3 and all questions, with attempts created to cover various dates but all
    passing. These attempts cover what should appear in the feed, with the exception of one as the feed only shows 10.
    """
    john = User.objects.get(id=1)
    sally = User.objects.get(id=2)
    alex = User.objects.get(id=3)

    program_question = Question.objects.get(slug='program-question-1')
    functions_question = Question.objects.get(slug='function-question-1')
    parsons_question = Question.objects.get(slug='parsons-question-1')
    debugging_question = Question.objects.get(slug='debugging-question-1')

    attempt1 = Attempt.objects.create(profile=john.profile, question=program_question, passed_tests=True,
                                      datetime=datetime.datetime(2020, 10, 1, 12, 21))
    attempt2 = Attempt.objects.create(profile=sally.profile, question=parsons_question, passed_tests=True,
                                      datetime=datetime.datetime(2020, 9, 21, 17, 0))
    attempt3 = Attempt.objects.create(profile=sally.profile, question=program_question, passed_tests=True,
                                      datetime=datetime.datetime(2020, 12, 23, 4, 44))
    attempt4 = Attempt.objects.create(profile=john.profile, question=debugging_question, passed_tests=True,
                                      datetime=datetime.datetime(2020, 4, 8, 1, 54))
    attempt5 = Attempt.objects.create(profile=alex.profile, question=debugging_question, passed_tests=True,
                                      datetime=datetime.datetime(2020, 1, 1, 0, 0))
    attempt6 = Attempt.objects.create(profile=john.profile, question=parsons_question, passed_tests=True,
                                      datetime=datetime.datetime(2020, 7, 2, 21, 8))
    attempt7 = Attempt.objects.create(profile=alex.profile, question=parsons_question, passed_tests=True,
                                      datetime=datetime.datetime(2020, 2, 7, 0, 31))
    attempt8 = Attempt.objects.create(profile=alex.profile, question=functions_question, passed_tests=True,
                                      datetime=datetime.datetime(2020, 9, 21, 18, 30))
    attempt9 = Attempt.objects.create(profile=alex.profile, question=program_question, passed_tests=True,
                                      datetime=datetime.datetime(2020, 11, 20, 11, 36))
    attempt10 = Attempt.objects.create(profile=sally.profile, question=debugging_question, passed_tests=True,
                                       datetime=datetime.datetime(2020, 5, 11, 9, 11))
    attempt11 = Attempt.objects.create(profile=john.profile, question=functions_question, passed_tests=True,
                                       datetime=datetime.datetime(2020, 1, 14, 16, 45))

    attempts = [attempt1, attempt2, attempt3, attempt4, attempt5, attempt6, attempt7, attempt8, attempt9, attempt10,
                attempt11]
    for attempt in attempts:
        attempt.save()
    return attempts


def generate_feed_attempts_failed_tests():
    """
    Generate attempts for codeWOF tests.

    Attempts are generated for users 1 to 3 and some questions, with attempts created to cover various dates but all
    failing. Despite being more recent that the attempts in generate_feed_attempts, they should not appear in the feed
    as they did not pass the tests.
    """
    john = User.objects.get(id=1)
    sally = User.objects.get(id=2)
    alex = User.objects.get(id=3)

    program_question = Question.objects.get(slug='program-question-1')
    parsons_question = Question.objects.get(slug='parsons-question-1')
    debugging_question = Question.objects.get(slug='debugging-question-1')

    Attempt.objects.create(profile=sally.profile, question=parsons_question, passed_tests=False,
                           datetime=datetime.datetime(2021, 9, 21, 17, 30)).save()
    Attempt.objects.create(profile=john.profile, question=program_question, passed_tests=False,
                           datetime=datetime.datetime(2021, 11, 3, 8, 12)).save()
    Attempt.objects.create(profile=alex.profile, question=debugging_question, passed_tests=False,
                           datetime=datetime.datetime(2021, 4, 19, 9, 50)).save()


def generate_feed_attempts_non_member():
    """
    Generate attempts for codeWOF tests.

    Attempts are generated for user 4 and some questions, with attempts created to cover various dates but all under a
    member unaffiliated with Group 1. Despite being more recent that the attempts in generate_feed_attempts, they
    should not appear in the feed as the user is not in Group 1.
    """
    jane = User.objects.get(id=4)

    program_question = Question.objects.get(slug='program-question-1')
    parsons_question = Question.objects.get(slug='parsons-question-1')

    Attempt.objects.create(profile=jane.profile, question=parsons_question, passed_tests=True,
                           datetime=datetime.datetime(2021, 9, 21, 17, 30)).save()
    Attempt.objects.create(profile=jane.profile, question=program_question, passed_tests=True,
                           datetime=datetime.datetime(2021, 11, 3, 8, 12)).save()


def generate_attempts_no_defaults():
    """
    Generate attempts for codeWOF tests.

    Always supplies the datetime to ensure consistent testing for test_send_email_reminders.py
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
    Generate study registration.

    Only user 1 is registered for the study.
    """
    user = User.objects.get(id=1)
    StudyRegistration.objects.create(
        user=user,
    )


def generate_users_with_notifications(user):
    """Generate users for codeWOF tests with notification days set. Creates two basic users for unit tests."""
    management.call_command("load_user_types")
    User.objects.create_user(
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

    User.objects.create_user(
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

    User.objects.create_user(
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

    User.objects.create_user(
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

    User.objects.create_user(
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

    User.objects.create_user(
        id=6,
        username='yankee',
        first_name='Yankee',
        last_name='Doodle',
        email='user6@uclive.ac.nz',
        password='onion',
        user_type=UserType.objects.get(slug='student'),
        remind_on_monday=True,
        remind_on_tuesday=False,
        remind_on_wednesday=False,
        remind_on_thursday=False,
        remind_on_friday=False,
        remind_on_saturday=False,
        remind_on_sunday=False,
        timezone="EST"
    )

    User.objects.create_user(
        id=7,
        username='odd',
        first_name='Odd',
        last_name='Ball',
        email='user7@uclive.ac.nz',
        password='onion',
        user_type=UserType.objects.get(slug='student'),
        remind_on_monday=True,
        remind_on_tuesday=False,
        remind_on_wednesday=False,
        remind_on_thursday=False,
        remind_on_friday=False,
        remind_on_saturday=False,
        remind_on_sunday=False,
        timezone="Asia/Kolkata"
    )

    User.objects.create_user(
        id=8,
        username='chatham',
        first_name='Chatham',
        last_name='Islands',
        email='user8@uclive.ac.nz',
        password='onion',
        user_type=UserType.objects.get(slug='student'),
        remind_on_monday=True,
        remind_on_tuesday=False,
        remind_on_wednesday=False,
        remind_on_thursday=False,
        remind_on_friday=False,
        remind_on_saturday=False,
        remind_on_sunday=False,
        timezone="Pacific/Chatham"
    )
