"""Custom loader for loading programming concepts."""

from django.db import transaction
from utils.TranslatableModelLoader import TranslatableModelLoader
from utils.errors import MissingRequiredFieldError
from programming.models import ProgrammingConcepts

TEST_CASE_FILE_TEMPLATE = 'test-case-{id}-{type}.txt'


class ProgrammingConceptsLoader(TranslatableModelLoader):
    """Custom loader for loading programming concepts."""

    def __init__(self, base_path="", structure_dir="structure", content_path="",
                 structure_filename="", lite_loader=False):
        """Create a BaseLoader object.

        Args:
            base_path (str): path to content_root, eg. "topics/content/".
            structure_dir (str): name of directory under base_path storing structure files.
            content_path (str): path within locale/structure dir to content directory, eg. "binary-numbers/unit-plan".
            structure_filename (str): name of yaml file, eg. "unit-plan.yaml".
            lite_loader (bool): Boolean to state whether loader should only
                be loading key content and perform minimal checks."
        """
        super().__init__(base_path, structure_dir, content_path, structure_filename, lite_loader)
        self.concepts_translations = dict()
        self.required_translation_fields = ["name"]

    @transaction.atomic
    def load(self):
        """Load programming concepts.

        Raise:
            MissingRequiredFieldError: when no object can be found with the matching
                attribute.
        """
        concept_structure = self.load_yaml_file(self.structure_file_path)
        self.concepts_translations = self.get_yaml_translations(
            self.structure_filename,
            required_fields=self.required_translation_fields,
            required_slugs=concept_structure.keys()
        )

        loaded_concepts = []
        for (concept_slug, concept_data) in concept_structure.items():
            loaded_concepts += self.load_concept_with_children(concept_slug, concept_data, None, 1)

        _, result = ProgrammingConcepts.objects.exclude(slug__in=loaded_concepts).delete()
        if result.get('programming.ProgrammingConcepts', 0) > 0:
            self.log('Deleted {} programming concepts(s)'.format(result['programming.ProgrammingConcepts']))

        self.log("All concepts loaded!\n")

    def load_concept_with_children(self, concept_slug, concept_data, parent, indent_level):
        """Load a programming concept and its children.
           Returns a list of all concepts loaded.
        """
        loaded_concepts = [concept_slug]
        concept_number = None
        if indent_level == 1:
            try:
                concept_number = concept_data['number']
            except KeyError:
                raise MissingRequiredFieldError(
                    self.structure_file_path,
                    [
                        'number',
                    ],
                    'Concepts'
                )

        defaults = dict()
        if concept_number:
            defaults["number"] = concept_number
        elif parent:
            defaults["number"] = parent.number

        if parent:
            defaults["parent"] = parent

        defaults["indent_level"] = indent_level

        defaults["has_children"] = "children" in concept_data

        concept, created = ProgrammingConcepts.objects.update_or_create(
            slug=concept_slug,
            defaults=defaults,
        )

        concept_translations = self.concepts_translations.get(concept_slug, dict())

        self.populate_translations(concept, concept_translations)
        self.mark_translation_availability(concept, required_fields=self.required_translation_fields)
        concept.save()

        if created:
            verb_text = 'Added'
        else:
            verb_text = 'Updated'

        self.log(f'{verb_text} concept: {concept.name} at level {indent_level}')

        if "children" in concept_data:
            children_concepts = concept_data["children"]
            if children_concepts is None:
                raise MissingRequiredFieldError(
                    self.structure_file_path,
                    ["slug"],
                    "Child Programming Concept"
                )
            for child in children_concepts:
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
                loaded_concepts += self.load_concept_with_children(child_slug, child_data, concept, indent_level + 1)

        return loaded_concepts
