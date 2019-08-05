"""Admin configuration for research application."""

from django import forms
from django.contrib import admin
from research.models import (
    Study,
    StudyGroup,
    StudyRegistration,
)
from research.utils import get_consent_form_class


class StudyAdminForm(forms.ModelForm):

    class Meta:
        model = Study
        fields = '__all__'

    def clean(self):
        try:
            get_consent_form_class(self.cleaned_data.get('consent_form'))
        except AttributeError:
            raise forms.ValidationError('Consent form class does not exist.')
        return self.cleaned_data


class StudyAdmin(admin.ModelAdmin):
    """Admin view for a study."""

    form = StudyAdminForm
    list_display = ('title', 'start_date', 'end_date', 'visible')


class StudyGroupAdmin(admin.ModelAdmin):
    """Admin view for a study group."""

    list_display = ('title', 'study')


class StudyRegistrationAdmin(admin.ModelAdmin):
    """Admin view for a study registration."""

    list_display = ('datetime', 'send_study_results', 'get_study', 'get_user_pk')

    def get_study(self, obj):
        return obj.study_group.study.title

    def get_user_pk(self, obj):
        return obj.user.pk


admin.site.register(Study, StudyAdmin)
admin.site.register(StudyGroup, StudyGroupAdmin)
admin.site.register(StudyRegistration, StudyRegistrationAdmin)
