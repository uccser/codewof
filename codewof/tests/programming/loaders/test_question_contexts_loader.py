from django.test import TestCase

from programming.management.commands._QuestionContextsLoader import QuestionContextsLoader
from programming.models import QuestionContexts

class QuestionContextsLoaderTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loader_name = "question_contexts"
        self.BASE_PATH = "tests/programming/loaders/assets/question-contexts/"
    
    def test_multiple_contexts(self):
        config_file = "multiple-contexts.yaml"
        loader = QuestionContextsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()
        self.assertQuerysetEqual(
            list(QuestionContexts.objects.all()),
            [
                "<QuestionContexts: Context 1>",
                "<QuestionContexts: Context 2>",
                "<QuestionContexts: Context 3>",
                "<QuestionContexts: Context 4>",
            ],
        )

    def test_insert_start(self):
        config_file = "multiple-contexts.yaml"
        loader = QuestionContextsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        config_file = "insert-start.yaml"
        loader = QuestionContextsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        self.assertQuerysetEqual(
            list(QuestionContexts.objects.all()),
            [
                "<QuestionContexts: Context 0>",
                "<QuestionContexts: Context 1>",
                "<QuestionContexts: Context 2>",
                "<QuestionContexts: Context 3>",
                "<QuestionContexts: Context 4>",
            ],
        )

    def test_delete_end(self):
        config_file = "multiple-contexts.yaml"
        loader = QuestionContextsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        config_file = "delete-end.yaml"
        loader = QuestionContextsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        self.assertQuerysetEqual(
            list(QuestionContexts.objects.all()),
            [
                "<QuestionContexts: Context 1>",
                "<QuestionContexts: Context 2>",
                "<QuestionContexts: Context 3>",
            ],
        )

    def test_child_contexts_load_properly(self):
        config_file = "child-contexts.yaml"
        loader = QuestionContextsLoader(
            structure_filename=config_file,
            base_path=self.BASE_PATH,
        )
        loader.load()

        print(QuestionContexts.objects.all())

        self.assertQuerysetEqual(
            list(QuestionContexts.objects.all()),
            [
                "<QuestionContexts: Advanced Geometry>",
                "<QuestionContexts: Advanced Mathematics>",
                "<QuestionContexts: Basic Geometry>",
                "<QuestionContexts: Geometry>",
                "<QuestionContexts: Mathematics>",
                "<QuestionContexts: Simple Mathematics>",
            ],
        )
