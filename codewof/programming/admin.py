"""Admin configuration for programming."""

from django.contrib import admin
from django.contrib.auth import get_user_model
from programming.models import (
    Attempt,
    TestCaseAttempt,
    QuestionTypeProgram,
    QuestionTypeFunction,
    QuestionTypeParsons,
    QuestionTypeDebugging,
    Profile,
    Badge,
    Earned,
)

User = get_user_model()


class TestCaseAttemptInline(admin.TabularInline):
    """Configuration for displaying test case attempts inline in admin."""

    model = TestCaseAttempt
    fields = ()
    extra = 0
    can_delete = False


class EarnedInline(admin.TabularInline):
    """Configuration to show earned badges inline within profile admin."""

    model = Earned
    extra = 1


class ProfileAdmin(admin.ModelAdmin):
    """Configuration for displaying profiles in admin."""

    list_display = ('user', 'points', 'goal', 'has_backdated')
    list_filter = ['goal', 'has_backdated']
    ordering = ('user', )
    inlines = (EarnedInline, )


class BadgeAdmin(admin.ModelAdmin):
    """Configuration for displaying badges in admin."""

    list_display = ('id_name', 'display_name', 'badge_tier')
    list_filter = ['badge_tier']
    ordering = ('id_name', )


class EarnedAdmin(admin.ModelAdmin):
    """Configuration for displaying earned badges in admin."""

    list_display = ('date', 'badge', 'profile')
    list_filter = ['badge']
    ordering = ('-date', )


class AttemptAdmin(admin.ModelAdmin):
    """Configuration for displaying attempts in admin."""

    list_display = ('datetime', 'question', 'profile', 'passed_tests')
    list_filter = ['passed_tests', 'question']
    ordering = ('-datetime', )
    inlines = (TestCaseAttemptInline, )

    class Media:
        """Add extra CSS rules."""

        css = {
            "all": ("css/admin.css",)
        }


admin.site.register(Attempt, AttemptAdmin)
admin.site.register(QuestionTypeProgram)
admin.site.register(QuestionTypeFunction)
admin.site.register(QuestionTypeParsons)
admin.site.register(QuestionTypeDebugging)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(Earned, EarnedAdmin)
