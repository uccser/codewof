"""Forms for user application."""

from django.forms import ModelForm
from django.contrib.auth import get_user_model, forms

User = get_user_model()


class SignupForm(ModelForm):
    """Sign up for user registration."""

    class Meta:
        """Metadata for SignupForm class."""

        model = get_user_model()
        fields = ['first_name', 'last_name']

    def signup(self, request, user):
        """Extra logic when a user signs up.

        Required by django-allauth.
        """
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class UserChangeForm(forms.UserChangeForm):
    """Form class for changing user."""

    class Meta(forms.UserChangeForm.Meta):
        """Metadata for UserChangeForm class."""

        model = User
        fields = ('email', 'last_name')


class UserCreationForm(forms.UserCreationForm):
    """Form class for creating user."""

    class Meta(forms.UserCreationForm.Meta):
        """Metadata for UserCreationForm class."""

        model = User
        fields = ('email', 'first_name', 'last_name')
