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

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Question)
admin.site.register(TestCase)
admin.site.register(SkillArea)
admin.site.register(Token)
admin.site.register(QuestionType)
admin.site.register(Badge)
admin.site.register(Earned)
admin.site.register(Attempt)
admin.site.register(Skill)
admin.site.register(LoginDay)