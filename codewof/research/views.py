"""Views for research application."""

from django.core.mail import send_mail
from django.template.loader import get_template
from django.templatetags.static import static
from django.views import generic
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAdminUser
from research.forms import ResearchConsentForm
from research.models import StudyRegistration
from research.utils import get_study_for_context
from research.serializers import StudyRegistrationSerializer


class StudyDetailView(LoginRequiredMixin, generic.TemplateView):
    """Page for the research study."""

    template_name = 'research/study_detail.html'

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)
        context['study'] = get_study_for_context()
        if self.request.user.is_authenticated:
            try:
                registration = StudyRegistration.objects.get(
                    user=self.request.user
                )
            except ObjectDoesNotExist:
                registration = None
        context['registration'] = registration
        return context


class StudyConsentFormView(LoginRequiredMixin, FormView):
    """Consent form for a research study."""

    form_class = ResearchConsentForm
    template_name = 'research/study_consent_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Check if consent form can be viewed."""
        try:
            StudyRegistration.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('research:home')

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)
        context['study'] = get_study_for_context()
        return context

    def form_valid(self, form):
        """Additional steps after form is validated.

        Args:
            form (Form): The valid form object.
        """
        # Create study registration object
        study = get_study_for_context()
        registration = StudyRegistration.objects.create(
            user=self.request.user,
            send_study_results=form.cleaned_data.get('send_study_results', False)
        )
        send_mail(
            'CodeWOF Research Consent Confirmation',
            self.build_email_plain(study, form, registration),
            settings.DEFAULT_FROM_EMAIL,
            [self.request.user.email],
            fail_silently=False,
            html_message=self.build_email_html(study, form, registration)
        )
        messages.success(
            self.request,
            'You are successfully enrolled into the {} study. You have been emailed a copy of your signed consent form.'.format(study['title'])  # noqa: E501
        )
        return redirect('research:home')

    def build_email_plain(self, study, form, registration):
        """
        Construct plaintext for the email body.

        :param study: This study.
        :param form: The form for this study.
        :param registration: The study registration of the user for this study.
        :return: The rendered HTML.
        """
        message = f"Dear {self.request.user.first_name}\n\n" \
                  f"Thank you for registering for the \"{study['title']}\" study. " \
                  f"Below is a copy of the information sheet, and your signed consent form.\n\n" \
                  f"{study['description']}\n\n" \
                  "Consent Form\n"
        for field in form:
            message += ("I AGREE" if field.value() else "I DO NOT AGREE") + f" - {field.label}\n"
        message += f"\nEmail address: {self.request.user.email}\n" \
                   f"Date: {registration.datetime}\n\n" \
                   "Thank you,\nThe codeWOF team"
        return message

    def build_email_html(self, study, form, registration):
        """
        Construct HTML for the email body using the consent_confirm.html template.

        :param study: This study.
        :param form: The form for this study.
        :param registration: The study registration of the user for this study.
        :return: The rendered HTML.
        """
        email_template = get_template("research/email/consent_confirm.html")
        return email_template.render(
            {"user": self.request.user, "study": study, "form": form, "registration": registration,
             "DOMAIN": settings.CODEWOF_DOMAIN})


class ResearcherPermission(permissions.BasePermission):
    """Global permission check if the user is a researcher of the study."""

    def has_object_permission(self, request, view, study):
        """Check if user is researcher of study."""
        user = request.user
        if user in study.researchers.all():
            return True
        else:
            return False


class StudyRegistrationAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows study registrations to be viewed."""

    permission_classes = [IsAdminUser]
    serializer_class = StudyRegistrationSerializer
    queryset = StudyRegistration.objects.all()
