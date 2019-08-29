"""Module for admin configuration for the users application."""

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from users.models import UserType
from users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


class UserAdmin(auth_admin.UserAdmin):
    """Custom user admin class."""

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = [
        'email',
        'first_name',
        'last_name',
        'user_type',
        'is_superuser',
    ]
    ordering = [
        'first_name',
        'last_name',
        'email',
    ]


admin.site.register(User, UserAdmin)
admin.site.register(UserType)
