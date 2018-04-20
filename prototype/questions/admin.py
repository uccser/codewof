from django.contrib import admin

from .models import Question, SkillArea, TestCase


admin.site.register(Question)
admin.site.register(TestCase)
admin.site.register(SkillArea)