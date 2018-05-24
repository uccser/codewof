from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


SMALL = 100
LARGE = 500

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    points = models.IntegerField()

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, points=0)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Token(models.Model):
    name = models.CharField(max_length=SMALL, primary_key=True)
    token = models.CharField(max_length=LARGE)

    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(max_length=SMALL)
    question_text = models.CharField(max_length=LARGE)
    question_type = models.SmallIntegerField()
    function_name = models.CharField(max_length=SMALL, blank=True)
    test_cases = models.ManyToManyField('TestCase')
    skill_areas = models.ManyToManyField('SkillArea', related_name='questions')

    def __str__(self):
        return self.title


class SkillArea(models.Model):
    name = models.CharField(max_length=SMALL)

    def __str__(self):
        return self.name


class TestCase(models.Model):
    function_params = models.CharField(max_length=LARGE, blank=True)
    test_input = models.CharField(max_length=LARGE, blank=True)
    expected_output = models.CharField(max_length=LARGE, blank=True)
    expected_return = models.CharField(max_length=LARGE, blank=True)

    def __str__(self):
        i, f, o, r = '', '', '', ''
        if len(self.test_input) > 0:
            i = self.test_input
            if len(self.function_params) > 0:
                i += ' + '
        if len(self.function_params) > 0:           
            f = 'f(' + self.function_params + ')'
        if len(self.expected_output) > 0:
            o = '"' + self.expected_output + '"'
            if len(self.expected_return) > 0:
                o += ' + '
        if len(self.expected_return) > 0:
            r = '(' + self.expected_return + ')'
        return i + f + ' -> ' + o + r