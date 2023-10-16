""" Forms for programming pages """

from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Button, Div, HTML, Field
from crispy_forms.bootstrap import Modal
from programming.models import Draft, DifficultyLevel

QUESTION_TYPE_CHOICES = [
    ('program', 'Program'),
    ('function', 'Function'),
    ('parsons', 'Parsons'),
    ('debugging', 'Debugging'),
]
QUESTION_DIFFICULTY_CHOICES = [
    (1, 'Easy'),
    (2, 'Moderate'),
    (3, 'Difficult'),
    (4, 'Complex'),
]
TEST_CASE_TYPES = [
    ('normal', 'Normal'),
    ('exceptional', 'Exceptional')
]
CONCEPTS = {
    "root": [
        ('display-text','Display Text'),
        ('functions','Functions'),
        ('inputs','Inputs'),
        ('conditionals','Conditionals'),
        ('loops','Loops'),
        ('string-operations','String Operations'),
        ('lists','Lists'),
    ],
    "conditionals": [
        ('single-condition','Single Condition'),
        ('multiple-conditions','Multiple Conditions'),
        ('advanced-conditionals','Advanced Conditionals'),
    ],
    "loops": [
        ('conditional-loops','Conditional Loops'),
        ('range-loops','Range Loops'),
    ],
}
CONTEXTS = {
    "root": [
        ("mathematics", "Mathematics"),
        ("real-world-applications", "Real World Applications"),
    ],
    "mathematics": [
        ("simple-mathematics", "Simple Mathematics"),
        ("advanced-mathematics", "Advanced Mathematics"),
    ],
    "geometry": [
        ("basic-geometry", "Basic Geometry"),
        ("advanced-geometry", "Advanced Geometry"),
    ],
}

class MacroForm(forms.Form):
    """Form for creating/editing macros for new questions"""
    name = forms.CharField(required=True, max_length='20')
    possible_values = forms.CharField(widget=forms.Textarea, required=True, help_text='Separate values with a comma (i.e. 6,7). You can escape commas with a backslash (i.e. 6\,7)')

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Modal(
                'name',
                'possible_values',
                Button(
                    "close_modal",
                    "Cancel",
                    id="close_modal",
                    css_class="btn mt-3",
                    data_toggle="modal",
                    data_target="#macro_modal",
                ),
                Button(
                    "save_var",
                    "Save Macro",
                    css_id="btn_macro_save",
                    css_class="btn-primary mt-3",
                ),
                css_id="macro_modal",
                title="Randomised Macro",
                title_class="w-100 text-center",
            ),
        )

class TestCaseForm(forms.Form):
    """Form for creating/editing test cases for new questions"""
    testcase_type = forms.ChoiceField(required=True, label='Type', choices=TEST_CASE_TYPES)
    testcase_code = forms.CharField(widget=forms.Textarea, label='Input Code', required=True)

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Modal(
                'testcase_type',
                'testcase_code',
                HTML('<small class="form-text text-muted font-italic">Expected output is generated from your provided solution code.</small>'),
                Button(
                    "close_modal",
                    "Cancel",
                    id="close_modal",
                    css_class="btn mt-3",
                    data_toggle="modal",
                    data_target="#test_case_modal",
                ),
                Button(
                    "save_test_case",
                    "Save Test Case",
                    css_id="btn_test_case_save",
                    css_class="btn-primary mt-3",
                ),
                css_id="test_case_modal",
                title="Test Case",
                title_class="w-100 text-center",
            ),
        )

class NewQuestionForm(forms.ModelForm):
    """Form for creating or editing new questions."""
    macros = forms.CharField(widget=forms.Textarea, required=False)
    initial_code = forms.CharField(widget=forms.Textarea, required=False)
    read_only_lines_top = forms.IntegerField(required=False, help_text="The number of lines at the top of the initial code to make read-only")
    read_only_lines_bottom = forms.IntegerField(required=False, help_text="The number of lines at the bottom of the initial code to make read-only")
    lines = forms.CharField(widget=forms.Textarea, required=False, label="Extra lines", help_text="Lines to mix in with solution lines")
    test_cases = forms.CharField(widget=forms.Textarea, required=False, help_text="Drag test cases up and down to reorder them (may not work with touch devices)")

    concepts = forms.MultipleChoiceField(required=False, choices=CONCEPTS["root"], widget=forms.CheckboxSelectMultiple(), label=False)
    concept_conditionals = forms.ChoiceField(required=False, choices=CONCEPTS["conditionals"], widget=forms.RadioSelect, label=False)
    concept_loops = forms.ChoiceField(required=False, choices=CONCEPTS["loops"], widget=forms.RadioSelect, label=False)

    contexts = forms.MultipleChoiceField(required=False, choices=CONTEXTS["root"], widget=forms.CheckboxSelectMultiple(), label=False)
    context_has_geometry = forms.BooleanField(required=False, initial=False, label="Geometry")
    context_mathematics = forms.ChoiceField(required=False, choices=CONTEXTS["mathematics"], widget=forms.RadioSelect, label=False)
    context_geometry = forms.ChoiceField(required=False, choices=CONTEXTS["geometry"], widget=forms.RadioSelect, label=False)

    difficulty_level = forms.ChoiceField(required=False, choices=QUESTION_DIFFICULTY_CHOICES, initial=QUESTION_DIFFICULTY_CHOICES[0], label='Difficulty')

    class Meta:
        model = Draft
        fields = ["title", "question_type", "difficulty_level", "question_text", "macros", "solution", "concepts", "contexts", "lines"]
        labels = {
            "title": "Question Title",
            "question_type": "Type",
        }
        widgets = {
            "question_type": forms.Select(choices=QUESTION_TYPE_CHOICES),
        }



    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # self.helper.form_action = ''
        self.helper.layout = Layout(
            'title',
            'question_type',
            'difficulty_level',
            'question_text',
            'macros',
            Div(
                Div(
                    HTML('{% include "programming/question_creation/macros_display_table.html" %}'),
                    css_class = "table-responsive",
                ),
                Button(
                    "new_macro",
                    "New macro",
                    css_id="btn_new_macro",
                    css_class="btn-outline-secondary",
                    type="button",
                ),
                css_class = "text-center",
            ),
            'solution',
            HTML('{% include "programming/question_components/indentation-warning.html" %}'),
            'initial_code',
            'read_only_lines_top',
            'read_only_lines_bottom',
            'lines',
            Modal(
                'concepts',
                'concept_conditionals',
                'concept_loops',
                Button(
                    "close_modal",
                    "Return to question",
                    css_id="btn_save_concepts",
                    css_class="btn-primary ml-auto mt-3",
                    data_toggle="modal",
                    data_target="#concept_modal",
                ),
                css_id="concept_modal",
                title="Concepts",
                title_class="w-100 text-center",
            ),
            Modal(
                'contexts',
                'context_has_geometry',
                'context_mathematics',
                'context_geometry',
                Button(
                    "close_modal",
                    "Return to question",
                    css_id="btn_save_contexts",
                    css_class="btn-primary ml-auto mt-3",
                    data_toggle="modal",
                    data_target="#context_modal",
                ),
                css_id="context_modal",
                title="Contexts",
                title_class="w-100 text-center",
            ),
            Div(
                HTML('{% include "programming/question_creation/tag_modal_indicators.html" %}'),
            ),
            'test_cases',
            Div(
                Div(
                    HTML('{% include "programming/question_creation/creation_test_case_table.html" %}'),
                    css_class = "table-responsive",
                    css_id = "test_case_table_container",
                ),
                Button(
                    "new_test_case",
                    "New test case",
                    css_id="btn_new_test_case",
                    css_class="btn-outline-secondary",
                    type="button",
                ),
                css_class = "text-center",
            ),
            Div(
                HTML(f'<a href = "{reverse("programming:draft_list")}" class="btn btn-outline-secondary">Cancel</a>'),
                Submit('submit', 'Save Question', css_class='ml-3'),
                css_class='button-tray mt-3',
            ),
        )

    def clean(self, *args, **kwargs):
        """
        Overrides the validation, as difficulty level is a foreign key and would otherwise
        raise an error.
        """
        cleaned_data = self.cleaned_data
        cleaned_data['difficulty_level'] = DifficultyLevel.objects.get(
            pk=cleaned_data['difficulty_level']
        )

        return cleaned_data
