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
    print(result_text)
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
    feedback_html = []
    for line in result_text.split('\n'):
        line_html = process_line(line)
        if line_html:
            feedback_html.append(line_html)
    result_data = {
        'feedback_html': feedback_html,
        'error_count': len(feedback_html),
    }
    return result_data


def process_line(line_text):
    line_html = ''
    re_result = re.search(LINE_RE, line_text)
    if re_result:
        line_number = re_result.group('line')
        char_number = re_result.group('character')
        error_code = re_result.group('error_code')
        error_message = re_result.group('error_message')
        error_data = python_data.PYTHON_ERRORS.get(error_code)
        print(error_data)
        # Check if message requires rendering
        if error_data.get('templated'):
            error_title = render_title(error_data, error_message)
        else:
            error_title = error_data['title']
        print(error_title)
        line_html = render_to_string(
            'style/component/style_error.html',
            {
                'pep8_code': error_code,
                'title': error_title,
                'line_number': line_number,
                'explanation': error_data['explanation'],
            }
        )
    return line_html


def render_title(error_data, error_message):
    template = error_data['title']
    # Find character
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
