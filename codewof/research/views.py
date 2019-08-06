"""Views for research application."""

from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from research.models import (
    Study,
    StudyRegistration,
)
from research.utils import get_consent_form_class
from research.forms import MaintainingProgrammingSkills2019Form


class StudyListView(generic.ListView):
    """Homepage for research studies."""

    model = Study
    context_object_name = 'studies'
    template_name = 'research/home.html'

    def get_queryset(self):
        """Return studies objects for page.

        Returns:
            Study queryset.
        """
        studies = Study.objects.filter(visible=True).order_by('start_date')
        return studies


class StudyDetailView(generic.DetailView):
    """Homepage for research studies."""

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
        try:
            registration = StudyRegistration.objects.get(
                user=self.request.user,
                study_group__in=self.object.groups.all(),
            )
        except ObjectDoesNotExist:
            registration = None
        context['registration'] = registration
        return context

class StudyConsentFormView(LoginRequiredMixin, FormView):

    template_name = 'research/study_consent_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.study = Study.objects.get(
            pk=self.kwargs.get('pk'),
        )
        try:
            StudyRegistration.objects.get(
                user=self.request.user,
                study_group__in=self.study.groups.all(),
            )
        except ObjectDoesNotExist:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(self.study)

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)
        context['study'] = self.study
        return context

    def get_initial(self):
        initial = {
            'email_address': self.request.user.email
        }
        return initial

    def get_form_class(self):
        return get_consent_form_class(self.study.consent_form)

    def form_valid(self, form):
        study = Study.objects.get(
            pk=self.kwargs.get('pk'),
        )
        group = study.get_next_group()
        # Create study registration object
        StudyRegistration.objects.create(
            study_group=group,
            user=self.request.user,
            send_study_results=form.cleaned_data.get('send_study_results', False)
        )
        # send_mail(
        #     SUBJECT_TEMPLATE.format(subject),
        #     MESSAGE_TEMPLATE.format(message, name),
        #     settings.DEFAULT_FROM_EMAIL,
        #     [from_email],
        #     fail_silently=False,
        # )
        messages.success(
            self.request,
            'You are successfully enrolled into this study. You have been emailed a copy of your signed consent form.'.format(study.title)
        )
        return redirect(study)
