from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *

def get_question_type(question_id):
    question = Question.objects.get_subclass(pk=question_id)
    if isinstance(question, ProgrammingFunction):
        subclass = "Function Programming Question"
    elif isinstance(question, Programming):
        subclass = "Program Programming Question"
    elif isinstance(question, BuggyFunction):
        subclass = "Function Debugging Question"
    elif isinstance(question, Buggy):
        subclass = "Program Debugging Question"
    else:
        subclass = "Parsons Problem"
    return subclass

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class ProgramTestCaseInline(admin.StackedInline):
    model = TestCaseProgram
    extra = 1

class FunctionTestCaseInline(admin.StackedInline):
    model = TestCaseFunction
    extra = 1

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

class CustomGenericQuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'type_display')
    search_fields = ('title',)

    def type_display(self, obj):
        return get_question_type(obj.pk)

    type_display.short_description = "Question Type"

@admin.register(Question)
class CustomQuestionAdmin(CustomGenericQuestionAdmin):

    def render_change_form(self, request, context, *args, **kwargs):
        self.change_form_template = 'admin/change_form_with_help_text.html'

        if context['original']:
            pk = context['original'].pk
            question = Question.objects.get_subclass(pk=pk)
            subclass = get_question_type(pk)
            is_correct_type = not isinstance(question, Buggy) and not isinstance(question, Programming)
        else:
            is_correct_type = True

        extra = {
            'is_correct_type': is_correct_type,
            'error_message': 'This page is intended for editing Parsons Problems only. Please go to the ' + subclass + ' page to edit this question.',
            'help_text': 'To define which blocks are displayed, write the program in the correct order in the solution box. Use 2 spaces for each level of indentation. A distractor can be added by ending the line with #distractor'
        }
        context.update(extra)
        return super(CustomQuestionAdmin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(Programming)
class CustomProgramQuestionAdmin(CustomGenericQuestionAdmin):
    inlines = [ProgramTestCaseInline, ]

    def render_change_form(self, request, context, *args, **kwargs):
        self.change_form_template = 'admin/change_form_with_help_text.html'

        if context['original']:
            pk = context['original'].pk
            question = Question.objects.get_subclass(pk=pk)
            subclass = get_question_type(pk)
            is_correct_type = not isinstance(question, ProgrammingFunction)
        else:
            is_correct_type = True

        extra = {
            'is_correct_type': is_correct_type,
            'error_message': 'This page is intended for editing program-type programming questions only. Please go to the ' + subclass + ' page to edit this question.',
            'help_text': ''
        }
        context.update(extra)
        return super(CustomProgramQuestionAdmin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(Buggy)
class CustomBuggyAdmin(CustomGenericQuestionAdmin):

    def render_change_form(self, request, context, *args, **kwargs):
        self.change_form_template = 'admin/change_form_with_help_text.html'
        
        if context['original']:
            pk = context['original'].pk
            question = Question.objects.get_subclass(pk=pk)
            subclass = get_question_type(pk)
            is_correct_type = not isinstance(question, BuggyFunction)
        else:
            is_correct_type = True

        extra = {
            'is_correct_type': is_correct_type,
            'error_message': 'This page is intended for editing program-type debugging questions only. Please go to the ' + subclass + ' page to edit this question.',
            'help_text': ''
        }
        context.update(extra)
        return super(CustomBuggyAdmin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(ProgrammingFunction)
class CustomFunctionQuestionAdmin(CustomGenericQuestionAdmin):
    inlines = [FunctionTestCaseInline, ]
   

@admin.register(BuggyFunction)
class CustomBuggyFunctionQuestionAdmin(CustomGenericQuestionAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

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