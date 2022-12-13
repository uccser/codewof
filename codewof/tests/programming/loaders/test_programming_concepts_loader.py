from django.test import TestCase

from programming.management.commands._ProgrammingConceptsLoader import ProgrammingConceptsLoader
from programming.models import ProgrammingConcepts

class ProgrammingConceptsLoaderTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loader_name = "programming_concepts"
        self.BASE_PATH = "tests/programming/loaders/assets/programming-concepts/"

    def test_multiple_concepts(self):
        config_file = "multiple-concepts.yaml"
        loader = ProgrammingConceptsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()
        
        self.assertQuerysetEqual(
            ProgrammingConcepts.objects.all(),
            [
                "<ProgrammingConcepts: Concept 1>",
                "<ProgrammingConcepts: Concept 2>",
                "<ProgrammingConcepts: Concept 3>",
                "<ProgrammingConcepts: Concept 4>",
            ],
            ordered=False,
        )

    def test_insert_start(self):
        config_file = "multiple-concepts.yaml"
        loader = ProgrammingConceptsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        config_file = "insert-start.yaml"
        loader = ProgrammingConceptsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        self.assertQuerysetEqual(
            list(ProgrammingConcepts.objects.all()),
            [
                "<ProgrammingConcepts: Concept 0>",
                "<ProgrammingConcepts: Concept 1>",
                "<ProgrammingConcepts: Concept 2>",
                "<ProgrammingConcepts: Concept 3>",
                "<ProgrammingConcepts: Concept 4>",
            ],
        )

    def test_delete_end(self):
        config_file = "multiple-concepts.yaml"
        loader = ProgrammingConceptsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        config_file = "delete-end.yaml"
        loader = ProgrammingConceptsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        self.assertQuerysetEqual(
            list(ProgrammingConcepts.objects.all()),
            [
                "<ProgrammingConcepts: Concept 1>",
                "<ProgrammingConcepts: Concept 2>",
                "<ProgrammingConcepts: Concept 3>",
            ],
        )

    def test_child_concepts_load_properly(self):
        config_file = "child-concepts.yaml"
        loader = ProgrammingConceptsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        self.assertQuerysetEqual(
            list(ProgrammingConcepts.objects.all()),
            [
                "<ProgrammingConcepts: Advanced Conditionals>",
                "<ProgrammingConcepts: Conditionals>",
                "<ProgrammingConcepts: Multiple Conditions>",
                "<ProgrammingConcepts: Single Condition>",
            ],
        )
