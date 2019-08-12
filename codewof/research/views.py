"""Views for research application."""

from django.views import generic
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from mail_templated import send_mail
from research.models import (
    Study,
    StudyRegistration,
)
from research.utils import get_consent_form_class


class StudyListView(LoginRequiredMixin, generic.ListView):
    """Homepage for research studies."""

    model = Study
    context_object_name = 'studies'
    template_name = 'research/home.html'

    def get_queryset(self):
        """Return studies objects for page.

        Returns:
            Study queryset.
        """
        studies = self.request.user.user_type.studies.all()
        # TODO: Simplify to one database query
        for study in studies:
            study.registered = StudyRegistration.objects.filter(
                user=self.request.user,
                study_group__in=study.groups.all(),
            ).exists()
        return studies


class StudyDetailView(LoginRequiredMixin, generic.DetailView):
    """Page for a research study."""

    model = Study
    context_object_name = 'study'

    def get_queryset(self):
        """Return studies objects for page.

        Returns:
            Study queryset.
        """
        studies = Study.objects.filter(visible=True).order_by('start_date')
        return studies

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)
        registration = None
        if self.request.user.is_authenticated:
            registration = StudyRegistration.objects.filter(
                user=self.request.user,
                study_group__in=self.object.groups.all(),
            ).first()
        context['registration'] = registration
        return context


class StudyConsentFormView(LoginRequiredMixin, FormView):
    """Consent form for a research study."""

    template_name = 'research/study_consent_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Check if consent form can be viewed."""
        self.study = Study.objects.get(
            pk=self.kwargs.get('pk'),
        )
        registration = None
        if self.request.user.is_authenticated:
            registration = StudyRegistration.objects.filter(
                user=self.request.user,
                study_group__in=self.study.groups.all(),
            ).first()

        if registration:
            return redirect(self.study)
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)
        context['study'] = self.study
        return context

    def get_form_class(self):
        """Get class for form."""
        return get_consent_form_class(self.study.consent_form)

    def form_valid(self, form):
        """Additional steps after form is validated.

        Args:
            form (Form): The valid form object.
        """
        study = Study.objects.get(
            pk=self.kwargs.get('pk'),
        )
        group = study.get_next_group()
        # Create study registration object
        registration = StudyRegistration.objects.create(
            study_group=group,
            user=self.request.user,
            send_study_results=form.cleaned_data.get('send_study_results', False)
        )
        send_mail(
            'research/email/consent_confirm.tpl',
            {
                'user': self.request.user,
                'study': study,
                'form': form,
                'registration': registration,
            },
            settings.DEFAULT_FROM_EMAIL,
            [self.request.user.email],
        )
        messages.success(
            self.request,
            'You are successfully enrolled into this study. You have been emailed a copy of your signed consent form.'.format(study.title)  # noqa: E501
        )
        return redirect(study)
