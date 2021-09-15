"""Custom loader for loading programming concepts."""

from os.path import join
from django.db import transaction
from utils.TranslatableModelLoader import TranslatableModelLoader
from utils.errors import (
    MissingRequiredFieldError,
    InvalidYAMLValueError,
)
from utils.language_utils import get_available_languages
from programming.models import ProgrammingConcepts

TEST_CASE_FILE_TEMPLATE = 'test-case-{id}-{type}.txt'


class ProgrammingConceptsLoader(TranslatableModelLoader):
    """Custom loader for loading programming concepts."""

    @transaction.atomic
    def load(self):
        """Load programming concepts.

        Raise:
            MissingRequiredFieldError: when no object can be found with the matching
                attribute.
        """
        concept_structure = self.load_yaml_file(self.structure_file_path)

        concept_translations = self.get_blank_translation_dictionary()
        required_translation_fields = ["name"]
        concepts_translations = self.get_yaml_translations(
            self.structure_filename,
            required_fields=required_translation_fields,
            required_slugs=concept_structure.keys()
        )

        for (concept_slug, concept_data) in concept_structure.items():
            # Check test cases exist
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
            # Todo - handle parents and children
            concept_translations = concepts_translations.get(concept_slug, dict())

            defaults = dict()
            defaults["number"] = concept_number

            concept, created = ProgrammingConcepts.objects.update_or_create(
                slug=concept_slug,
                defaults=defaults,
            )

            self.populate_translations(concept, concept_translations)
            self.mark_translation_availability(concept, required_fields=required_translation_fields)
            concept.save()

            if created:
                verb_text = 'Added'
            else:
                verb_text = 'Updated'

            self.log(f'{verb_text} concept: {concept.name}')

             # Create children concepts with reference to parent
            if "children" in concept_data:
                children_concepts = concept_data["children"]
                if children_concepts is None:
                    raise MissingRequiredFieldError(
                        self.structure_file_path,
                        ["slug"],
                        "Child Programming Concept"
                    )
                for child_slug in children_concepts:
                    translations = concepts_translations.get(child_slug, dict())

                    new_child = ProgrammingConcepts(
                        slug=child_slug,
                        number=concept_number,
                        parent=concept,
                    )
                    self.populate_translations(new_child, translations)
                    self.mark_translation_availability(new_child, required_fields=["name"])

                    new_child.save()

                    self.log("Added child programming concept: {}".format(new_child.__str__()), 1)

        self.log("All concepts loaded!\n")
