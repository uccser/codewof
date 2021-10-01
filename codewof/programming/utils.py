from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Row,
    Column,
    Field,
    Div,
    HTML,
    Submit,
)

FILTER_HELPER_RESET_HTML_TEMPLATE = '<a href="{{% url "{}" %}}" class="btn btn-danger">Reset</a>'

def create_filter_helper(reset_url_pattern):
    """Return filter formatting helper.
    Args:
        reset_url_pattern (str): URL to set reset button to.
    Returns:
        Crispy-forms form helper.
    """
    filter_formatter = FormHelper()
    filter_formatter.form_method = 'get'
    filter_formatter.layout = Layout(
        Row(
            Column(
                Field(
                    'difficulty_level',
                    css_class='form-control form-control-sm',
                ),
                css_class='col-sm-12 col-md-4 mb-0',
            ),
            Column(
                Field(
                    'concepts',
                    css_class='form-control form-control-sm',
                ),
                css_class='form-group col-sm-12 col-md-4 mb-0',
            ),
            Column(
                Field(
                    'contexts',
                    css_class='form-control form-control-sm',
                ),
                css_class='form-group col-sm-12 col-md-4 mb-0',
            ),
        ),
        Div(
            HTML(FILTER_HELPER_RESET_HTML_TEMPLATE.format(reset_url_pattern)),
            Submit('submit', 'Filter questions', css_class='btn-success'),
            css_class='d-flex justify-content-between',
        )
    )
    return filter_formatter