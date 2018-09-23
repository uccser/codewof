from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

class ProgramTestCaseInline(admin.StackedInline):
    model = TestCaseProgram
    extra = 1

@admin.register(Programming)
class CustomProgramQuestionAdmin(admin.ModelAdmin):
    inlines = [ProgramTestCaseInline, ]

class FunctionTestCaseInline(admin.StackedInline):
    model = TestCaseFunction
    extra = 1

@admin.register(ProgrammingFunction)
class CustomFunctionQuestionAdmin(admin.ModelAdmin):
    inlines = [FunctionTestCaseInline, ]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Question)
admin.site.register(Buggy)
admin.site.register(BuggyFunction)

admin.site.register(TestCase)
admin.site.register(TestCaseFunction)
admin.site.register(TestCaseProgram)

admin.site.register(SkillArea)
admin.site.register(Token)
admin.site.register(Badge)
admin.site.register(Earned)
admin.site.register(Attempt)
admin.site.register(Skill)
admin.site.register(LoginDay)