"""Forms for user application."""

from django import forms
from django.contrib import auth
from django.urls import reverse
from django.utils.translation import gettext as _
from users.models import UserType, Group
from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Fieldset, ButtonHolder, Button, Field, Div

User = auth.get_user_model()
POLICY_STATEMENT = '<p>By clicking Sign Up, you agree to our <a href="{0}#terms-of-service">Terms</a>, <a href="{0}#privacy-policy">Privacy Policy</a> and <a href="{0}#cookie-policy">Cookie Policy</a>.</p>'  # noqa E501


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
    captcha = ReCaptchaField()

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
            'captcha',
            HTML(POLICY_STATEMENT.format(reverse('general:policies'))),
            Submit('submit', 'Sign Up', css_class="btn-success"),
        )

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
            ButtonHolder(
                Submit('submit', 'Update', css_class='btn btn-primary')
            ),
        )

    class Meta:
        """Metadata for UserChangeForm class."""

        model = User
        fields = ('first_name', 'last_name', 'user_type', 'remind_on_monday', 'remind_on_tuesday',
                  'remind_on_wednesday', 'remind_on_thursday', 'remind_on_friday', 'remind_on_saturday',
                  'remind_on_sunday')


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

    class Meta:
        model = Group
        fields = ('name', 'description')
