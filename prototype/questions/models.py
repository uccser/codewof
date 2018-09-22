from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator


SMALL = 100
LARGE = 500

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    points = models.IntegerField(default=0)
    goal = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    earned_badges = models.ManyToManyField('Badge', through='Earned')
    attempted_questions = models.ManyToManyField('Question', through='Attempt')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, points=0)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class LoginDay(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    day = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.day)

class Badge(models.Model):
    name = models.CharField(max_length=SMALL)
    description = models.CharField(max_length=LARGE)

    def __str__(self):
        return self.name


class Earned(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    badge = models.ForeignKey('Badge', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date)

class Token(models.Model):
    name = models.CharField(max_length=SMALL, primary_key=True)
    token = models.CharField(max_length=LARGE)

    def __str__(self):
        return self.name


class Attempt(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    user_code = models.TextField()
    passed_tests = models.BooleanField(default=False)
    is_save = models.BooleanField(default=False)
    skills_hinted = models.ManyToManyField('Skill', blank=True)

    def __str__(self):
        return "Attempted '" + str(self.question) + "' on " + str(self.date)


class Question(models.Model):
    title = models.CharField(max_length=SMALL)
    question_text = models.TextField()
    solution = models.TextField(blank=True)
    buggy_program = models.TextField(blank=True)
    question_type = models.ForeignKey('QuestionType', on_delete=models.CASCADE)
    function_name = models.CharField(max_length=SMALL, blank=True)
    test_cases = models.ManyToManyField('TestCase')
    skill_areas = models.ManyToManyField('SkillArea', related_name='questions')
    skills = models.ManyToManyField('Skill', blank=True)

    def __str__(self):
        return self.title


class QuestionType(models.Model):
    name = models.CharField(max_length=SMALL)
    
    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=SMALL)
    hint = models.CharField(max_length=LARGE)
    subskills = models.ManyToManyField('self', symmetrical=False, blank=True) 

    def __str__(self):
        return self.name

class SkillArea(models.Model):
    name = models.CharField(max_length=SMALL)

    def __str__(self):
        return self.name


class TestCase(models.Model):
    function_params = models.CharField(max_length=LARGE, blank=True)
    test_input = models.CharField(max_length=LARGE, blank=True)
    expected_output = models.CharField(max_length=LARGE, blank=True)
    expected_return = models.CharField(max_length=LARGE, blank=True, null=True)

    def __str__(self):
        i, f, o, r = '', '', '', ''
        i = str(self.test_input)
        i += ' + '    
        f = 'f(' + str(self.function_params) + ')'
    
        o = '"' + str(self.expected_output) + '"'
        o += ' + '
        r = '(' + str(self.expected_return) + ')'
        return i + f + ' -> ' + o + r