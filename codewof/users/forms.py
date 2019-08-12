"""Forms for user application."""

from django import forms
from django.contrib import auth
from users.models import UserType
from django.utils.translation import gettext as _

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

    def signup(self, request, user):
        """Extra logic when a user signs up.

        Required by django-allauth.
        """
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_type = self.cleaned_data['user_type']
        user.save()


class UserChangeForm(auth.forms.UserChangeForm):
    """Form class for changing user."""

    class Meta(auth.forms.UserChangeForm.Meta):
        """Metadata for UserChangeForm class."""

        model = User
        fields = ('email', 'last_name', 'user_type')


class UserCreationForm(auth.forms.UserCreationForm):
    """Form class for creating user."""

    class Meta(auth.forms.UserCreationForm.Meta):
        """Metadata for UserCreationForm class."""

        model = User
        fields = ('email', 'first_name', 'last_name', 'user_type')
