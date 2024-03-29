from django.test import TestCase

from users.forms import UserChangeForm, GroupCreateUpdateForm, GroupInvitationsForm
from django.core import management

from users.models import UserType


class UserFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        management.call_command("load_user_types")

    def test_required_fields_only(self):
        form_data = {"first_name": "John", "last_name": "Doe", "user_type": UserType.objects.get(slug='student').pk,
                     "timezone": "Pacific/Auckland"}
        form = UserChangeForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_required_fields_and_notification_days(self):
        form_data = {"first_name": "John", "last_name": "Doe", "user_type": UserType.objects.get(slug='student').pk,
                     "remind_on_monday": True, "remind_on_tuesday": False, "remind_on_wednesday": False,
                     "remind_on_thursday": True, "remind_on_friday": False, "remind_on_saturday": False,
                     "remind_on_sunday": False, "timezone": "Pacific/Auckland"}
        form = UserChangeForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_required_fields_and_all_notification_days(self):
        form_data = {"first_name": "John", "last_name": "Doe", "user_type": UserType.objects.get(slug='teacher').pk,
                     "remind_on_monday": True, "remind_on_tuesday": True, "remind_on_wednesday": True,
                     "remind_on_thursday": True, "remind_on_friday": True, "remind_on_saturday": True,
                     "remind_on_sunday": True, "timezone": "Pacific/Auckland"}
        form = UserChangeForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_required_fields_and_no_notification_days(self):
        form_data = {"first_name": "John", "last_name": "Doe", "user_type": UserType.objects.get(slug='other').pk,
                     "remind_on_monday": False, "remind_on_tuesday": False, "remind_on_wednesday": False,
                     "remind_on_thursday": False, "remind_on_friday": False, "remind_on_saturday": False,
                     "remind_on_sunday": False, "timezone": "Pacific/Auckland"}
        form = UserChangeForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_first_name_required(self):
        form = UserChangeForm(data={"first_name": ""})

        self.assertEqual(form.errors["first_name"], ["This field is required."])

    def test_last_name_required(self):
        form = UserChangeForm(data={"last_name": ""})

        self.assertEqual(form.errors["last_name"], ["This field is required."])

    def test_invalid_timezone(self):
        form = UserChangeForm(data={"timezone": "Pacific/Wellington"})

        self.assertEqual(form.errors["timezone"],
                         ["Select a valid choice. Pacific/Wellington is not one of the available choices."])


class TestGroupCreateUpdateForm(TestCase):
    def test_name_and_description_and_feed_enabled_works(self):
        form_data = {"name": "Group", "description": "Group description", "feed_enabled": True}
        form = GroupCreateUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_name_only_works(self):
        form_data = {"name": "Group"}
        form = GroupCreateUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_missing_name_does_not_work(self):
        form_data = {"description": "Group description", "feed_enabled": False}
        form = GroupCreateUpdateForm(data=form_data)

        self.assertEqual(form.errors["name"], ["This field is required."])

    def test_name_too_long(self):
        form_data = {"name": "x" * 51, "description": "Group description"}
        form = GroupCreateUpdateForm(data=form_data)

        self.assertTrue(form.errors["name"], ["This field is required."])

    def test_name_length_boundary(self):
        form_data = {"name": "x" * 50, "description": "Group description"}
        form = GroupCreateUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_description_too_long(self):
        form_data = {"name": "Group", "description": "x" * 201}
        form = GroupCreateUpdateForm(data=form_data)

        self.assertTrue(form.errors["description"], ["This field is required."])

    def test_description_length_boundary(self):
        form_data = {"name": "Group", "description": "x" * 200}
        form = GroupCreateUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())


class TestGroupInvitationsForm(TestCase):
    def test_single_email_is_valid(self):
        form_data = {"emails": "test@mail.com"}
        form = GroupInvitationsForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_empty_emails_is_invalid(self):
        form_data = {"emails": ""}
        form = GroupInvitationsForm(data=form_data)

        self.assertTrue(form.errors["emails"], ["This field is required."])

    def test_white_space_emails_is_invalid(self):
        form_data = {"emails": "   \n   "}
        form = GroupInvitationsForm(data=form_data)

        self.assertTrue(form.errors["emails"], ["This field is required."])

    def test_missing_emails_is_invalid(self):
        form_data = {}
        form = GroupInvitationsForm(data=form_data)

        self.assertTrue(form.errors["emails"], ["This field is required."])
