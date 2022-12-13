from django.test import TestCase

from programming.management.commands._DifficultiesLoader import DifficultiesLoader
from programming.models import DifficultyLevel


class DifficultiesLoaderTest(TestCase):
    """Tests for the DifficultiesLoader."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loader_name = "difficulties"
        self.BASE_PATH = "tests/programming/loaders/assets/difficulties/"

    def test_multiple_difficulties(self):
        config_file = "multiple-difficulties.yaml"
        loader = DifficultiesLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()
        self.assertQuerysetEqual(
            DifficultyLevel.objects.all(),
            [
                "<DifficultyLevel: Easy>",
                "<DifficultyLevel: Moderate>",
                "<DifficultyLevel: Difficult>",
                "<DifficultyLevel: Complex>",
            ],
            ordered=False,
        )

    def test_insert_start(self):
        config_file = "multiple-difficulties.yaml"
        loader = DifficultiesLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        config_file = "insert-start.yaml"
        loader = DifficultiesLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        self.assertQuerysetEqual(
            DifficultyLevel.objects.all(),
            [
                "<DifficultyLevel: Trivial>",
                "<DifficultyLevel: Easy>",
                "<DifficultyLevel: Moderate>",
                "<DifficultyLevel: Difficult>",
                "<DifficultyLevel: Complex>",
            ],
            ordered=False,
        )

    def test_delete_end(self):
        config_file = "multiple-difficulties.yaml"
        loader = DifficultiesLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        config_file = "remove-end.yaml"
        loader = DifficultiesLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        self.assertQuerysetEqual(
            DifficultyLevel.objects.all(),
            [
                "<DifficultyLevel: Easy>",
                "<DifficultyLevel: Moderate>",
                "<DifficultyLevel: Difficult>",
            ],
            ordered=False,
        )
