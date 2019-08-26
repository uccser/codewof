"""Admin configuration for programming."""

from django.contrib import admin
from django.contrib.auth import get_user_model
from programming.models import Attempt, TestCaseAttempt

User = get_user_model()


class TestCaseAttemptInline(admin.TabularInline):
    model = TestCaseAttempt
    fields = ()
    extra = 0
    can_delete = False


class AttemptAdmin(admin.ModelAdmin):
    """Configuration for displaying attempts in admin."""

    list_display = ('datetime', 'question', 'profile', 'passed_tests')
    ordering = ('-datetime', )
    inlines = (TestCaseAttemptInline, )

    class Media:
        """Add extra CSS rules."""

        css = {
            "all": ("css/admin.css",)
        }


admin.site.register(Attempt, AttemptAdmin)
