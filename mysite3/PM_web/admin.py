
from PM_web.models import *

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
# Register your models here.
admin.site.register(Profile)
admin.site.register(Team_information)
admin.site.register(Operator)
class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = 'profile_detail_information'
class UserAdmin(admin.ModelAdmin):
	inlines = [ProfileInline]
admin.site.unregister(User)
admin.site.register(User,UserAdmin)

class TeamInline(admin.StackedInline):
	model = Team_information
	can_delete = False
	verbose_name_plural = 'Group_details'

class GroupAdmin(admin.ModelAdmin):
	inlines = [TeamInline]
admin.site.unregister(Group)
admin.site.register(Group,GroupAdmin)


#@admin.register(User)
#class UserAdmin(admin.ModelAdmin):
#    inlines = [ProfileInline]
