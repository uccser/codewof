# from django.core.management.base import BaseCommand
# from questions.models import *

# NAME = "Bitfit 1"

# TEXT = "Make your program calculate the area of a rectangle given a width of 13 and length of 217. The area is the width multiplied by the length.\n\
# Then print the area."

# SOL = "width = 13\n\
# length = 217\n\
# area = width * length\n\
# print(area)"


# class Command(BaseCommand):
#     help = "look in management/commands"

#     def _create_questions(self):
#         function = QuestionType.objects.get(name='Function')
#         program = QuestionType.objects.get(name='Program')

#         test = TestCase(expected_output="2821\n", expected_return="", test_input="", function_params="")
#         test.full_clean()        
#         test.save()

#         question = Question(title=NAME, question_text=TEXT, question_type=program, solution=SOL)
#         question.full_clean()
#         question.save()
#         question.test_cases.add(test)


#     def handle(self, *args, **options):
#         self._create_questions()