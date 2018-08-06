from django.core.management.base import BaseCommand
from questions.models import *

class Command(BaseCommand):
    help = "look in management/commands"

    def _create_questions(self):
        function = QuestionType.objects.get(name='Function')
        question = Question(title='Test', question_text='Hello\nworld', question_type=function, solution='A\n solution')
        question.save()

    def handle(self, *args, **options):
        self._create_questions()