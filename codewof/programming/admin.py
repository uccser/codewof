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
    model = Earned
    extra = 1


class ProfileAdmin(admin.ModelAdmin):
    inlines = (EarnedInline, )


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
admin.site.register(QuestionTypeProgram)
admin.site.register(QuestionTypeFunction)
admin.site.register(QuestionTypeParsons)
admin.site.register(QuestionTypeDebugging)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Badge)
