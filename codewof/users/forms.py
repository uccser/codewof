"""Forms for user application."""

from django import forms
from django.contrib import auth
from django.urls import reverse
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from users.models import UserType, Group
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Fieldset, ButtonHolder, Button, Div

User = auth.get_user_model()


class SignupForm(forms.Form):
    """Sign up for user registration."""

    first_name = forms.CharField(
        max_length=50,
        label='First name',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'placeholder': _('First name'),
            },
        ),
    )
    last_name = forms.CharField(
        max_length=150,
        label='Last name',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'placeholder': _('Last name'),
            },
        ),
    )
    user_type = forms.ModelChoiceField(
        queryset=UserType.objects.all(),
        label='Are you a student or teacher?',
        empty_label=None,
    )
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'email',
            'first_name',
            'last_name',
            'user_type',
            'password1',
            'password2',
            HTML(render_to_string('account/signup-declarations.html')),
            'captcha',
            HTML(render_to_string('account/recaptcha-declaration.html')),
            Submit('submit', 'Sign Up', css_class="btn-success"),
        )
        self.fields['captcha'].label = False

    def signup(self, request, user):
        """Extra logic when a user signs up.

        Required by django-allauth.
        """
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_type = self.cleaned_data['user_type']
        user.save()


class UserChangeForm(forms.ModelForm):
    """Form class for changing user."""

    user_type = forms.ModelChoiceField(
        queryset=UserType.objects.all(),
        label='Are you a student or teacher?',
        empty_label=None,
    )

    remind_on_monday = forms.BooleanField(required=False, label='Monday')
    remind_on_tuesday = forms.BooleanField(required=False, label='Tuesday')
    remind_on_wednesday = forms.BooleanField(required=False, label='Wednesday')
    remind_on_thursday = forms.BooleanField(required=False, label='Thursday')
    remind_on_friday = forms.BooleanField(required=False, label='Friday')
    remind_on_saturday = forms.BooleanField(required=False, label='Saturday')
    remind_on_sunday = forms.BooleanField(required=False, label='Sunday')

    timezone = forms.ChoiceField(
        choices=User.TIMEZONES,
        label='What is your timezone? (Used to schedule email reminders)',
    )

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML("<h2>Details</h2>"),
            Fieldset(
                None,
                'first_name',
                'last_name',
                'user_type',
            ),
            HTML("<h2>Emails</h2>"),
            Button('emails', 'Manage your email addresses', css_class='btn btn-outline-primary',
                   onclick="window.location.href = '{}';".format(reverse('account_email'))),

            Div(
                HTML("<p id=\"notifications-p\">Send me notifications on:</p>"),
                'remind_on_monday',
                'remind_on_tuesday',
                'remind_on_wednesday',
                'remind_on_thursday',
                'remind_on_friday',
                'remind_on_saturday',
                'remind_on_sunday'
            ),
            Fieldset(
                None,
                'timezone',
            ),
            ButtonHolder(
                Submit('submit', 'Update', css_class='btn btn-primary')
            ),
        )

    class Meta:
        """Metadata for UserChangeForm class."""

        model = User
        fields = ('first_name', 'last_name', 'user_type', 'remind_on_monday', 'remind_on_tuesday',
                  'remind_on_wednesday', 'remind_on_thursday', 'remind_on_friday', 'remind_on_saturday',
                  'remind_on_sunday', 'timezone')


class UserAdminChangeForm(auth.forms.UserChangeForm):
    """Form class for changing user."""

    class Meta(auth.forms.UserChangeForm.Meta):
        """Metadata for UserAdminChangeForm class."""

        model = User
        fields = ('email', 'last_name', 'user_type')


class UserAdminCreationForm(auth.forms.UserCreationForm):
    """Form class for creating user."""

    class Meta(auth.forms.UserCreationForm.Meta):
        """Metadata for UserAdminCreationForm class."""

        model = User
        fields = ('email', 'first_name', 'last_name', 'user_type')


class GroupCreateUpdateForm(forms.ModelForm):
    """Form class for creating or updating a group."""

    name = forms.CharField(
        max_length=Group._meta.get_field('name').max_length,
        label='Name',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'placeholder': _('Name'),
            },
        ),
        required=not Group._meta.get_field('name').blank
    )

    description = forms.CharField(
        max_length=Group._meta.get_field('description').max_length,
        label='Description',
        widget=forms.Textarea(
            attrs={
                'type': 'text',
                'placeholder': _('Description'),
            },
        ),
        required=not Group._meta.get_field('description').blank
    )

    feed_enabled = forms.BooleanField(
        label='Enable Feed?',
        required=False
    )

    class Meta:
        """Metadata for GroupCreateUpdateForm class."""

        model = Group
        fields = ('name', 'description', 'feed_enabled')


class GroupInvitationsForm(forms.Form):
    """Form class for sending out invitations to join a group."""

    emails = forms.CharField(
        label='Emails one per line',
        widget=forms.Textarea(
            attrs={
                'type': 'text',
            },
        ),
    )
