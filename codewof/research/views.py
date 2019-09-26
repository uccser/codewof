"""Views for research application."""

import csv
from django.views import generic
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.shortcuts import redirect, get_object_or_404
from mail_templated import send_mail
from programming.models import Attempt
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from research.serializers import StudySerializer
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
        studies = self.request.user.user_type.studies.filter(
            visible=True,
            groups__isnull=False,
        ).distinct()
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
        """Return studies objects to select study from.

        Returns:
            Study queryset.
        """
        studies = Study.objects.filter(
            visible=True,
            groups__isnull=False,
        ).distinct()
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
        if self.request.user in self.object.researchers.all():
            context['researcher'] = True
        context['registration'] = registration
        return context


class StudyAdminView(LoginRequiredMixin, generic.DetailView):
    """Admin page for a research study."""

    model = Study
    context_object_name = 'study'
    template_name = 'research/study_admin.html'

    def get_queryset(self):
        """Return queryset for selecting study from."""
        return self.request.user.studies_researching.all()


def study_admin_csv_download_view(request, pk):
    """Admin view for downloading research study data as a CSV."""
    study = get_object_or_404(
        request.user.studies_researching,
        pk=pk,
    )
    field_order = [
        'datetime',
        'id',
        'question_id',
        'user_code',
        'passed_tests',
        'profile__user__pk',
        'profile__user__email',
    ]
    filename = 'somefilename.csv'

    # Create HttpResponse object with CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    writer = csv.DictWriter(response, fieldnames=field_order)
    writer.writeheader()

    for group in study.groups.all():
        for registration in group.registrations.all():
            attempts = Attempt.objects.filter(
                profile=registration.user.profile,
                datetime__gt=registration.datetime,
                datetime__date__lte=study.end_date,
            ).values(
                'datetime',
                'id',
                'question_id',
                'user_code',
                'passed_tests',
                'profile__user__pk',
                'profile__user__email',
            )
            writer.writerows(attempts)
    return response


class StudyConsentFormView(LoginRequiredMixin, FormView):
    """Consent form for a research study."""

    template_name = 'research/study_consent_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Check if consent form can be viewed."""
        self.study = Study.objects.filter(
            pk=self.kwargs.get('pk'),
            visible=True,
            groups__isnull=False,
        ).distinct().first()
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


class StudyAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows studies to be viewed."""

    permission_classes = [IsAdminUser]
    queryset = Study.objects.all()
    serializer_class = StudySerializer
