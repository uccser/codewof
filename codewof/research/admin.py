"""Admin configuration for research application."""

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from research.models import (
    Study,
    StudyGroup,
    StudyRegistration,
)
from programming.models import Question
from research.utils import get_consent_form_class


class StudyAdminForm(forms.ModelForm):
    """Form for admin view for a study."""

    class Meta:
        """Meta attributes for class."""

        model = Study
        fields = '__all__'

    def clean(self):
        """Validate admin model submission."""
        try:
            get_consent_form_class(self.cleaned_data.get('consent_form'))
        except AttributeError:
            raise forms.ValidationError('Consent form class does not exist.')
        return self.cleaned_data


class StudyAdmin(admin.ModelAdmin):
    """Admin view for a study."""

    form = StudyAdminForm
    list_display = ('title', 'start_date', 'end_date', 'visible')
    filter_horizontal = ('user_types', )


class StudyGroupForm(forms.ModelForm):
    """Form for admin view for a study group."""

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.select_subclasses(),
        widget=FilteredSelectMultiple(
            verbose_name='Questions',
            is_stacked=False,
        ),
    )

    class Meta:
        """Meta attributes for class."""

        model = StudyGroup
        fields = '__all__'


class StudyGroupAdmin(admin.ModelAdmin):
    """Admin view for a study group."""

    form = StudyGroupForm
    list_display = ('title', 'study')
    filter_horizontal = ('questions', )


class StudyRegistrationAdmin(admin.ModelAdmin):
    """Admin view for a study registration."""

    list_display = ('datetime', 'send_study_results', 'study_name', 'user_id')

    def study_name(self, obj):
        """Get name of study."""
        return obj.study_group.study.title

    def user_id(self, obj):
        """Get ID of user."""
        return obj.user.pk


admin.site.register(Study, StudyAdmin)
admin.site.register(StudyGroup, StudyGroupAdmin)
admin.site.register(StudyRegistration, StudyRegistrationAdmin)
