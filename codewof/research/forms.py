"""Forms for the research application."""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Div


class ResearchConsentForm(forms.Form):
    """Consent form for current reseach.

    If not in use, in empty with 'pass'.
    """

    condition_1 = forms.BooleanField(
        required=True,
        label='I have been given a full explanation of this project and have had the opportunity to ask questions.'
    )
    condition_2 = forms.BooleanField(
        required=True,
        label='I understand what is required of me if I agree to take part in the research.'
    )
    condition_3 = forms.BooleanField(
        required=True,
        label='I understand that participation is voluntary and I may withdraw at any time without penalty. Withdrawal of participation will also include the withdrawal of any information I have provided should this remain practically achievable.'  # noqa: E501
    )
    condition_4 = forms.BooleanField(
        required=True,
        label='I understand that any information or opinions I provide will be kept confidential to the researcher and her supervisor and that any published or reported results will not identify the participants. I understand that the report for this research project will be made available on the UC website.'  # noqa: E501
    )
    condition_5 = forms.BooleanField(
        required=True,
        label='I understand that all data collected for the study will be kept in password protected electronic form and will be destroyed after five years.'  # noqa: E501
    )
    condition_6 = forms.BooleanField(
        required=True,
        label='I understand that I can contact the researcher Lucy Turner at ltt19@uclive.ac.nz or supervisor Tim Bell at tim.bell@canterbury.ac.nz for further information. If I have any complaints, I can contact the Chair of the University of Canterbury Educational Research Human Ethics Committee, Private Bag 4800, Christchurch (human-ethics@canterbury.ac.nz).'  # noqa: E501
    )
    condition_7 = forms.BooleanField(
        required=True,
        label='I confirm that I am at least 18 years old and have programmed in Python before.'
    )
    send_study_results = forms.BooleanField(
        required=False,
        label='(Optional) I would like a summary of the results of the project to be emailed to me.'
    )
    condition_8 = forms.BooleanField(
        required=True,
        label='By clicking “I agree” below, I agree to participate in this research project.'
    )

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'condition_1',
            'condition_2',
            'condition_3',
            'condition_4',
            'condition_5',
            'condition_6',
            'condition_7',
            'send_study_results',
            'condition_8',
            Div(
                HTML(
                    '<a class="btn btn-secondary" href={% url "research:home" %}>'
                    'I do not agree'
                    '</a>'
                ),
                Submit('submit', 'I agree', css_class='btn-success'),
                css_class='d-flex justify-content-around my-5',
            ),
        )
