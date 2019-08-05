"""Admin configuration for research application."""

from django.contrib import admin
from research.models import (
    Study,
    StudyGroup,
    StudyRegistration
)


class StudyAdmin(admin.ModelAdmin):
    """Admin view for a study."""

    list_display = ('title', 'start_date', 'end_date', 'visible')


admin.site.register(Study, StudyAdmin)
admin.site.register(StudyGroup)
admin.site.register(StudyRegistration)
