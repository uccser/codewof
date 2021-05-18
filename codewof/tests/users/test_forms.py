from django.test import TestCase

from users.forms import UserChangeForm
from django.core import management

from users.models import UserType


class UserFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        management.call_command("load_user_types")

    def test_required_fields_only(self):
        form_data = {"first_name": "John", "last_name": "Doe", "user_type": UserType.objects.get(slug='student').pk}
        form = UserChangeForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_required_fields_and_notification_days(self):
        form_data = {"first_name": "John", "last_name": "Doe", "user_type": UserType.objects.get(slug='student').pk,
                     "remind_on_monday": True, "remind_on_tuesday": False, "remind_on_wednesday": False,
                     "remind_on_thursday": True, "remind_on_friday": False, "remind_on_saturday": False,
                     "remind_on_sunday": False}
        form = UserChangeForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_required_fields_and_all_notification_days(self):
        form_data = {"first_name": "John", "last_name": "Doe", "user_type": UserType.objects.get(slug='teacher').pk,
                     "remind_on_monday": True, "remind_on_tuesday": True, "remind_on_wednesday": True,
                     "remind_on_thursday": True, "remind_on_friday": True, "remind_on_saturday": True,
                     "remind_on_sunday": True}
        form = UserChangeForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_required_fields_and_no_notification_days(self):
        form_data = {"first_name": "John", "last_name": "Doe", "user_type": UserType.objects.get(slug='other').pk,
                     "remind_on_monday": False, "remind_on_tuesday": False, "remind_on_wednesday": False,
                     "remind_on_thursday": False, "remind_on_friday": False, "remind_on_saturday": False,
                     "remind_on_sunday": False}
        form = UserChangeForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_first_name_required(self):
        form = UserChangeForm(data={"first_name": ""})

        self.assertEqual(form.errors["first_name"], ["This field is required."])

    def test_last_name_required(self):
        form = UserChangeForm(data={"last_name": ""})

        self.assertEqual(form.errors["last_name"], ["This field is required."])
