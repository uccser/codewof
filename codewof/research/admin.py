"""Admin configuration for research application."""

from django.contrib import admin
from research.models import StudyRegistration


class StudyRegistrationAdmin(admin.ModelAdmin):
    """Admin view for a study registration."""

    list_display = ('datetime', 'send_study_results', 'user_id')

    def user_id(self, obj):
        """Get ID of user."""
        return obj.user.pk


admin.site.register(StudyRegistration, StudyRegistrationAdmin)
