from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


def get_question_type(question_id):
    """returns the type of question and the route to the appropriate admin page"""
    question = Question.objects.get_subclass(pk=question_id)
    link = "/admin/questions/"
    if isinstance(question, ProgrammingFunction):
        subclass = "Function Programming Question"
        link += "programmingfunction/"
    elif isinstance(question, Programming):
        subclass = "Programming Question"
        link += "programming/"
    elif isinstance(question, BuggyFunction):
        subclass = "Function Debugging Question"
        link += "buggyfunction/"
    elif isinstance(question, Buggy):
        subclass = "Debugging Question"
        link += "buggy/"
    else:
        subclass = "Parsons Problem"
        link += "question/"
    return (subclass, link)

### INLINES ###

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class ProgramTestCaseInline(admin.StackedInline):
    model = QuestionTypeProgramTestCase
    extra = 1

class FunctionTestCaseInline(admin.StackedInline):
    model = QuestionTypeFunctionTestCase
    extra = 1

### CUSTOM ADMINS ###

# class CustomUserAdmin(UserAdmin):
#     inlines = (ProfileInline, )

#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)

class CustomGenericQuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'type_display')
    search_fields = ('title',)

    def type_display(self, obj):
        subclass, _ = get_question_type(obj.pk)
        return subclass

    type_display.short_description = "Question Type"

# @admin.register(Question)
# class CustomQuestionAdmin(CustomGenericQuestionAdmin):

#     def render_change_form(self, request, context, *args, **kwargs):
#         self.change_form_template = 'admin/change_form_with_help_text.html'

#         if context['original']:
#             pk = context['original'].pk
#             question = Question.objects.get_subclass(pk=pk)
#             subclass, link = get_question_type(pk)
#             is_correct_type = not isinstance(question, Buggy) and not isinstance(question, Programming)
#         else:
#             subclass = ''
#             link = ''
#             is_correct_type = True

#         extra = {
#             'is_correct_type': is_correct_type,
#             'error_message_part_1': 'This page is intended for editing Parsons Problems only. Please go to the ',
#             'subclass': subclass,
#             'link': link,
#             'error_message_part_2': ' page to edit this question.',
#             'help_text': 'To define which blocks are displayed, write the program in the correct order in the solution box. Use 2 spaces for each level of indentation. A distractor can be added by ending the line with #distractor'
#         }
#         context.update(extra)
#         return super(CustomQuestionAdmin, self).render_change_form(request, context, *args, **kwargs)


# @admin.register(QuestionTypeProgram)
# class CustomProgramQuestionAdmin(CustomGenericQuestionAdmin):
#     inlines = [ProgramTestCaseInline, ]

#     def render_change_form(self, request, context, *args, **kwargs):
#         self.change_form_template = 'admin/change_form_with_help_text.html'

#         if context['original']:
#             pk = context['original'].pk
#             question = Question.objects.get_subclass(pk=pk)
#             subclass, link = get_question_type(pk)
#             is_correct_type = not isinstance(question, ProgrammingFunction)
#         else:
#             subclass = ''
#             link = ''
#             is_correct_type = True

#         extra = {
#             'is_correct_type': is_correct_type,
#             'error_message_part_1': 'This page is intended for editing program-type programming questions only. Please go to the ',
#             'subclass': subclass,
#             'link': link,
#             'error_message_part_2': ' page to edit this question.',
#             'help_text': 'When creating test cases, test input (stdin) and expected output (stdout) will always be strings so you do not need to put quotes around them. Any quotes you enter will be escaped.'
#         }
#         context.update(extra)
#         return super(CustomProgramQuestionAdmin, self).render_change_form(request, context, *args, **kwargs)


# @admin.register(Buggy)
# class CustomBuggyAdmin(CustomGenericQuestionAdmin):

#     def render_change_form(self, request, context, *args, **kwargs):
#         self.change_form_template = 'admin/change_form_with_help_text.html'

#         if context['original']:
#             pk = context['original'].pk
#             question = Question.objects.get_subclass(pk=pk)
#             subclass, link = get_question_type(pk)
#             is_correct_type = not isinstance(question, BuggyFunction)
#         else:
#             subclass = ''
#             link = ''
#             is_correct_type = True

#         extra = {
#             'is_correct_type': is_correct_type,
#             'error_message_part_1': 'This page is intended for editing program-type debugging questions only. Please go to the ',
#             'subclass': subclass,
#             'link': link,
#             'error_message_part_2': ' page to edit this question.',
#             'help_text': 'The buggy program is the one that will be shown to the user. It is important that the correct solution works and is different in some way to the buggy program.\nPlease indent using four spaces (not tabs).'
#         }
#         context.update(extra)
#         return super(CustomBuggyAdmin, self).render_change_form(request, context, *args, **kwargs)


# @admin.register(QuestionTypeFunction)
# class CustomFunctionQuestionAdmin(CustomGenericQuestionAdmin):
#     inlines = [FunctionTestCaseInline, ]

#     def render_change_form(self, request, context, *args, **kwargs):
#         self.change_form_template = 'admin/change_form_with_help_text.html'

#         extra = {
#             'is_correct_type': True,
#             'error_message_part_1': 'This page is intended for editing function-type programming questions only. Please go to the ',
#             'subclass': "",
#             'link': "",
#             'error_message_part_2': ' page to edit this question.',
#             'help_text': 'Remember to tell the user the function name somewhere in the question text.\nWhen creating test cases, test input (stdin) and expected output (stdout) will always be strings so you do not need to put quotes around them. Any quotes you enter will be escaped.\nHowever, for function params and expected return, the value needs to be valid Python so quotes around strings are necessary.\nFunction params are comma separated.'
#         }
#         context.update(extra)
#         return super(CustomFunctionQuestionAdmin, self).render_change_form(request, context, *args, **kwargs)


# @admin.register(BuggyFunction)
# class CustomBuggyFunctionQuestionAdmin(CustomGenericQuestionAdmin):
#     def render_change_form(self, request, context, *args, **kwargs):
#         self.change_form_template = 'admin/change_form_with_help_text.html'

#         extra = {
#             'is_correct_type': True,
#             'error_message_part_1': 'This page is intended for editing function-type debugging questions only. Please go to the ',
#             'subclass': "",
#             'link': "",
#             'error_message_part_2': ' page to edit this question.',
#             'help_text': 'The buggy program is the one that will be shown to the user. It is important that the correct solution works and is different in some way to the buggy program.\nPlease indent using four spaces (not tabs).'
#         }
#         context.update(extra)
#         return super(CustomBuggyFunctionQuestionAdmin, self).render_change_form(request, context, *args, **kwargs)


### FOR DEV PURPOSES ONLY ###
# @admin.register(TestCase)
# class TestCaseAdmin(admin.ModelAdmin):
#     form = TestCaseForm

class AttemptAdmin(admin.ModelAdmin):
    """Configuration for displaying attempts in admin."""

    list_display = ('datetime', 'question', 'profile', 'passed_tests')
    ordering = ('-datetime', )


# admin.site.register(SkillArea)
# admin.site.register(Token)
# admin.site.register(Badge)
# admin.site.register(Earned)
admin.site.register(QuestionTypeProgram)
admin.site.register(QuestionTypeProgramTestCase)
admin.site.register(QuestionTypeFunction)
admin.site.register(QuestionTypeFunctionTestCase)
admin.site.register(QuestionTypeParsons)
admin.site.register(QuestionTypeParsonsTestCase)
admin.site.register(Attempt, AttemptAdmin)
admin.site.register(TestCaseAttempt)
# admin.site.register(Skill)
# admin.site.register(LoginDay)
