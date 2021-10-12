"""Style checking code for Python 3 code."""

import re
import os.path
import uuid
import subprocess
from pathlib import Path
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from style.utils import (
    CHARACTER_DESCRIPTIONS,
    get_language_info,
    get_article,
)
from style.models import Error

LINE_RE = re.compile(r':(?P<line>\d+):(?P<character>\d+): (?P<error_code>\w\d+) (?P<error_message>.*)$')
CHARACTER_RE = re.compile(r'\'(?P<character>.*)\'')
TEMP_FILE_ROOT = settings.STYLE_CHECKER_TEMP_FILES_ROOT
TEMP_FILE_EXT = '.py'
# Create folder if it does not exist
Path(TEMP_FILE_ROOT).mkdir(parents=True, exist_ok=True)
PYTHON3_DETAILS = get_language_info('python3')


def python3_style_check(code):
    """Run the flake8 style check on provided code.

    Args:
        code (str): String of user code.

    Returns:
        List of dictionaries of style checker result data.
    """
    # Write file to HDD
    filename = str(uuid.uuid4()) + TEMP_FILE_EXT
    filepath = Path(os.path.join(TEMP_FILE_ROOT, filename))
    f = open(filepath, 'w')
    f.write(code)
    f.close()

    # Read file with flake8
    checker_result = subprocess.run(
        [
            'flake8',
            filepath,
            '--config=' + PYTHON3_DETAILS['checker-config'],
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Process results
    result_text = checker_result.stdout.decode('utf-8')
    is_example_code = code == PYTHON3_DETAILS['example_code']
    result_data = process_results(result_text, is_example_code)

    # Delete file from HDD
    filepath.unlink()

    # Send results
    return result_data


def process_results(result_text, is_example_code):
    """Process results into data for response.

    Args:
        result_text (str): Text output from style checker.
        is_example_code (bool): True if provided code matches the example code.

    Returns:
        List of dictionaries of result data.
    """
    issues = []
    for line in result_text.split('\n'):
        issue_data = process_line(line, is_example_code)
        if issue_data:
            issues.append(issue_data)
    return issues


def process_line(line_text, is_example_code):
    """
    Process style error by matching database entry and incrementing count.

    Note: Could at extracting parts of this function to a generic
          utility function.

    Args:
        line_text (str): Text of style checker result.
        is_example_code (bool): True if program was provided example code.

    Returns:
        Dictionary of information about style error.
    """
    issue_data = dict()
    re_result = re.search(LINE_RE, line_text)
    if re_result:
        line_number = re_result.group('line')
        error_code = re_result.group('error_code')
        error_message = re_result.group('error_message')

        try:
            error = Error.objects.get(
                language='python3',
                code=error_code,
            )
            # Increment error occurence count, if not example code
            if not is_example_code:
                error.count = F('count') + 1
                error.save()

            if error.title_templated:
                error_title = render_text(error.title, error_message)
                error_solution = render_text(error.solution, error_message)
            else:
                error_title = error.title
                error_solution = error.solution

            issue_data = {
                'code': error_code,
                'title': error_title,
                'line_number': line_number,
                'solution': error_solution,
                'explanation': error.explanation,
            }
        except ObjectDoesNotExist:
            # If error is not defined in database.
            issue_data = {
                'code': error_code,
                'title': error_message,
                'line_number': line_number,
            }
    return issue_data


def render_text(template, error_message):
    """Render title text from error message contents.

    Args:
        template (str): Template for formatting text.
        error_message (str): Original style error message.

    Returns:
        Rendered title text.
    """
    re_result = re.search(CHARACTER_RE, error_message)
    character = re_result.group('character')
    character_description = CHARACTER_DESCRIPTIONS[character]
    template_data = {
        'character': character,
        'character_description': character_description,
        'article': get_article(character_description),
    }
    title = template.format(**template_data)
    return title
