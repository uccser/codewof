from django.db import models

SMALL = 100
LARGE = 500

class Token(models.Model):
    name = models.CharField(max_length=SMALL, primary_key=True)
    token = models.CharField(max_length=LARGE)

    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(max_length=SMALL)
    question_text = models.CharField(max_length=LARGE)
    test_cases = models.ManyToManyField('TestCase')
    skill_areas = models.ManyToManyField('SkillArea', related_name='questions')

    def __str__(self):
        return self.question_text


class SkillArea(models.Model):
    name = models.CharField(max_length=SMALL)

    def __str__(self):
        return self.name


class TestCase(models.Model):
    test_input = models.CharField(max_length=SMALL)
    expected_output = models.CharField(max_length=LARGE)

    def __str__(self):
        return self.test_input + ' -> ' + self.expected_output