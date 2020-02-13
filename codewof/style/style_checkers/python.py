import re
import os.path
import uuid
import subprocess
from pathlib import Path
from django.conf import settings
from django.template.loader import render_to_string
from style.style_checkers import python_data


LINE_RE = re.compile(r':(?P<line>\d+):(?P<character>\d+): (?P<error_code>\w\d+) (?P<error_message>.*)$')
CHARACTER_RE = re.compile(r'\'(?P<character>.*)\'')
TEMP_FILE_ROOT = settings.STYLE_CHECKER_TEMP_FILES_ROOT
TEMP_FILE_EXT = '.py'
# Create folder if it does not exist
Path(TEMP_FILE_ROOT).mkdir(parents=True, exist_ok=True)

def python_style_check(code):
    # Write file to HDD
    filename = str(uuid.uuid4()) + TEMP_FILE_EXT
    filepath = Path(os.path.join(TEMP_FILE_ROOT, filename))
    f = open(filepath, 'w')
    f.write(code)
    f.close()

    # Read file with flake8
    checker_result = subprocess.run(
        [
            '/docker_venv/bin/flake8',
            filepath,
            '--config=' + settings.STYLE_CHECKER_PYTHON3_SETTINGS,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Process results
    result_text = checker_result.stdout.decode('utf-8')
    result_data = process_results(result_text)

    # Delete file from HDD
    filepath.unlink()

    # Send results
    return result_data


def process_results(result_text):
    """Process results into data for response.

    Args:
        result_text (str): Text output from style checker.

    Returns:
        List of dictionaries of result data.
    """
    issues = []
    for line in result_text.split('\n'):
        issue_data = process_line(line)
        if issue_data:
            issues.append(issue_data)
    # TODO: Check for at least one comment
    result_html = render_to_string(
        'style/component/feedback_result.html',
        {
            'issues': issues,
            'issue_count': len(issues),
        }
    )
    return result_html


def process_line(line_text):
    issue_data = dict()
    re_result = re.search(LINE_RE, line_text)
    if re_result:
        line_number = re_result.group('line')
        char_number = re_result.group('character')
        error_code = re_result.group('error_code')
        error_message = re_result.group('error_message')
        error_data = python_data.PYTHON_ISSUES.get(error_code, dict())
        if error_data.get('templated'):
            error_title = render_text(error_data['title'], error_message)
            error_solution = render_text(error_data['solution'], error_message)
        else:
            try:
                error_title = error_data['title']
                error_solution = error_data['solution']
            except KeyError:
                error_title = error_data.get('original_message', error_message)
                error_solution = ''
        # TODO: Link to https://www.flake8rules.com if available
        issue_data = {
            'error_code': error_code,
            'title': error_title,
            'line_number': line_number,
            'solution': error_solution,
            'explanation': error_data.get('explanation', ''),
        }
    return issue_data


def render_text(template, error_message):
    re_result = re.search(CHARACTER_RE, error_message)
    character = re_result.group('character')
    character_description = python_data.CHARACTER_DESCRIPTIONS[character]
    template_data  = {
        'character': character,
        'character_description': character_description,
        'article': python_data.get_article(character_description),
    }
    title = template.format(**template_data)
    return title
