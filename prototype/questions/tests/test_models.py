from django.test import TestCase

from questions.models import Question

class QuestionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        Question.objects.create(title='Test', question_text='Hello', question_type=1)

    def setUp(self):
        pass

    def test_question_text_label(self):
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('question_text').verbose_name
        self.assertEquals(field_label, 'question text')
    
    def test_question_type_label(self):
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('question_type').verbose_name
        self.assertEquals(field_label, 'question type')

    def test_question_text_length(self):
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('question_text').max_length
        self.assertEquals(max_length, 500)

    def test_str_question_is_title(self):
        question = Question.objects.get(id=1)
        self.assertEquals(str(question), question.title)