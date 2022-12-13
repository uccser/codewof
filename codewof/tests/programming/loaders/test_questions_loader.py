from django.test import TestCase as DjangoTestCase

from programming.management.commands._QuestionsLoader import QuestionsLoader
from programming.models import Question, DifficultyLevel, ProgrammingConcepts, TestCase

from utils.errors.InvalidYAMLValueError import InvalidYAMLValueError


class QuestionsLoaderTest(DjangoTestCase):
    """Tests for the QuestionsLoader."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loader_name = "questions"
        self.BASE_PATH = "tests/programming/loaders/assets/questions/"

    @classmethod
    def setUpTestData(cls):
        print("setting up test data")
        DifficultyLevel.objects.create(slug='difficulty-0', level=0, name='Difficulty 0')
        ProgrammingConcepts.objects.create(name='Display Text', slug='display-text', number=1)

    def test_multiple_questions(self):
        config_file = "multiple-questions.yaml"
        loader = QuestionsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()
        self.assertQuerysetEqual(
            list(Question.objects.all()),
            [
                "<Question: Say Hello!>",
                "<Question: Say Hello 2!>",
            ],
        )

    def test_insert_start(self):
        config_file = "multiple-questions.yaml"
        loader = QuestionsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        config_file = "insert-start.yaml"
        loader = QuestionsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        self.assertQuerysetEqual(
            list(Question.objects.all()),
            [
                "<Question: Say Hello 3!>",
                "<Question: Say Hello!>",
                "<Question: Say Hello 2!>",
            ],
        )

    def test_delete_end(self):
        config_file = "multiple-questions.yaml"
        loader = QuestionsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        config_file = "delete-end.yaml"
        loader = QuestionsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        self.assertQuerysetEqual(
            list(Question.objects.all()),
            [
                "<Question: Say Hello!>",
            ],
        )

    def test_multiple_test_cases(self):
        config_file = "multiple-test-cases.yaml"
        loader = QuestionsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        self.assertQuerysetEqual(
            list(TestCase.objects.all()),
            [
                "<TestCase: normal>",
                "<TestCase: normal>",
            ],
        )

    def test_insert_start_test_case(self):
        config_file = "multiple-test-cases.yaml"
        loader = QuestionsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        config_file = "insert-start-test-case.yaml"
        loader = QuestionsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        self.assertQuerysetEqual(
            list(TestCase.objects.all()),
            [
                "<TestCase: exceptional>",
                "<TestCase: normal>",
                "<TestCase: normal>",
            ],
        )

    def test_delete_end_test_case(self):
        config_file = "multiple-test-cases.yaml"
        loader = QuestionsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        self.assertQuerysetEqual(
            list(TestCase.objects.all()),
            [
                "<TestCase: normal>",
                "<TestCase: normal>",
            ],
        )

        config_file = "delete-end-test-case.yaml"
        loader = QuestionsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        self.assertQuerysetEqual(
            list(TestCase.objects.all()),
            [
                "<TestCase: normal>",
            ],
        )

    def test_test_case_numbers_order(self):
        config_file = "test-case-numbers-order.yaml"
        loader = QuestionsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )

        with self.assertRaises(InvalidYAMLValueError):
            loader.load()
