"""Module for the custom Django load_style_errors command."""

import importlib
from django.core import management
from verto import Verto
from verto.errors.Error import Error as VertoError
from style.utils import get_language_slugs
from style.models import Error
from utils.errors.VertoConversionError import VertoConversionError


BASE_DATA_MODULE_PATH = 'style.style_checkers.{}_data'
MARKDOWN_CONVERTER = Verto(
    extensions=[
        "markdown.extensions.fenced_code",
    ],
)

class Command(management.base.BaseCommand):
    """Required command class for the custom Django load_style_errors command."""

    help = "Load progress outcomes to database."

    def convert_markdown(self, module_path, code, field, markdown):
        MARKDOWN_CONVERTER.clear_saved_data()
        try:
            result = MARKDOWN_CONVERTER.convert(markdown)
        except VertoError as e:
            location = '{} - {} - {}'.format(module_path, code, field)
            raise VertoConversionError(location, e) from e
        return result.html_string

    def handle(self, *args, **options):
        """Automatically called when the load_style_errors command is given."""
        created_count = 0
        updated_count = 0

        for language_code in get_language_slugs():
            # Import langauge data
            module_path = BASE_DATA_MODULE_PATH.format(language_code)
            module = importlib.import_module(module_path)
            language_data = getattr(module, 'DATA')

            # Load errors into database
            for code, code_data in language_data.items():
                code_data['title'] = self.convert_markdown(
                    module_path,
                    code,
                    'title',
                    code_data['title'],
                )
                if code_data.get('solution'):
                    code_data['solution'] = self.convert_markdown(
                        module_path,
                        code,
                        'solution',
                        code_data['solution'],
                    )
                if code_data.get('explanation'):
                    code_data['explanation'] = self.convert_markdown(
                        module_path,
                        code,
                        'explanation',
                        code_data['explanation'],
                    )

                obj, created = Error.objects.update_or_create(
                    language=language_code,
                    code=code,
                    defaults=code_data,
                )
                if created:
                    created_count += 1
                    print('Created {}'.format(obj))
                else:
                    updated_count += 1
                    print('Updated {}'.format(obj))
        print('Style errors loaded ({} created, {} updated).'.format(created_count, updated_count))
