"""Custom loader for loading question contexts."""

from django.db import transaction
from utils.TranslatableModelLoader import TranslatableModelLoader
from utils.errors import (
    MissingRequiredFieldError,
)
from programming.models import QuestionContexts

TEST_CASE_FILE_TEMPLATE = 'test-case-{id}-{type}.txt'


class QuestionContextsLoader(TranslatableModelLoader):
    """Custom loader for loading question contexts."""

    def __init__(self, base_path="", structure_dir="structure", content_path="",
                 structure_filename="", lite_loader=False):
        """Create a QuestionContextLoader object.

        Args:
            base_path (str): path to content_root, eg. "topics/content/".
            structure_dir (str): name of directory under base_path storing structure files.
            content_path (str): path within locale/structure dir to content directory, eg. "binary-numbers/unit-plan".
            structure_filename (str): name of yaml file, eg. "unit-plan.yaml".
            lite_loader (bool): Boolean to state whether loader should only
                be loading key content and perform minimal checks."
        """
        super().__init__(base_path, structure_dir, content_path, structure_filename, lite_loader)
        self.contexts_translations = dict()
        self.required_translation_fields = ["name"]

    @transaction.atomic
    def load(self):
        """Load question contexts.

        Raise:
            MissingRequiredFieldError: when no object can be found with the matching
                attribute.
        """
        context_structure = self.load_yaml_file(self.structure_file_path)
        self.contexts_translations = self.get_yaml_translations(
            self.structure_filename,
            required_fields=self.required_translation_fields,
            required_slugs=context_structure.keys()
        )

        for (context_slug, context_data) in context_structure.items():
            self.load_single_context(context_slug, context_data, None, 1)
        self.log("All contexts loaded!\n")

    def load_single_context(self, context_slug, context_data, parent, indent_level):
        """Load a single context."""
        context_number = None
        if indent_level == 1:
            try:
                context_number = context_data['number']
            except KeyError:
                raise MissingRequiredFieldError(
                    self.structure_file_path,
                    [
                        'number',
                    ],
                    'Contexts'
                )

        defaults = dict()
        if context_number:
            defaults["number"] = context_number
        elif parent:
            defaults["number"] = parent.number

        if parent:
            defaults["parent"] = parent

        defaults["indent_level"] = indent_level

        context, created = QuestionContexts.objects.update_or_create(
            slug=context_slug,
            defaults=defaults,
        )

        context_translations = self.contexts_translations.get(context_slug, dict())

        self.populate_translations(context, context_translations)
        self.mark_translation_availability(context, required_fields=self.required_translation_fields)
        context.save()

        if created:
            verb_text = 'Added'
        else:
            verb_text = 'Updated'

        self.log(f'{verb_text} context: {context.name} at level {indent_level}')

        if "children" in context_data:
            children_contexts = context_data["children"]
            if children_contexts is None:
                raise MissingRequiredFieldError(
                    self.structure_file_path,
                    ["slug"],
                    "Child Question Context"
                )
            for child in children_contexts:
                if type(child) is dict:
                    child_data = dict()
                    for key in child.keys():
                        if key == "children":
                            child_data["children"] = child["children"]
                        else:
                            child_slug = key
                else:
                    child_slug = child
                    child_data = []
                self.load_single_context(child_slug, child_data, context, indent_level + 1)
