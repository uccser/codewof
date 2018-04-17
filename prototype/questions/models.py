from django.db import models

# Create your models here.
class Question(models.Model):
    title = models.CharField(max_length=100)
    question_text = models.CharField(max_length=500)

    def __str__(self):
        return self.question_text