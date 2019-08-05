from django import forms


class MaintainingProgrammingSkills2019Form(forms.Form):
    """Consent form for Maintaining Programming Skills study."""

    condition_1 = forms.BooleanField(
        required=True,
        label='I have been given a full explanation of this project and have had the opportunity to ask questions.'
    )
