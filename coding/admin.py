from django.contrib import admin

# Register your models here.

from .models import *


class ExtendInline(admin.StackedInline):
	model = CodeQuestionExtend

class TestCaseInline(admin.TabularInline):
	model = CodeTestCase
	extra  = 3

class CodeQuestionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,               {'fields': ['question_text']}),
	]
	inlines = [ExtendInline,TestCaseInline]
	def save_model(self, request, obj, form, change):
		obj.type = 'code'
		obj.save()


class CodeUserStatusAdmin(admin.ModelAdmin):
    '''
        Admin View for CodeUserStatus
    '''
    list_display = ('User','question','question_status','remaining_time')
    list_filter = ('question_status',)


class UserSubmissionAdmin(admin.ModelAdmin):
    '''
        Admin View for UserSubmission
    '''
    list_display = ('User','question','ith_test_case_failed','rmin','rsec')
    list_filter = ('User','question')

admin.site.register(UserSubmission, UserSubmissionAdmin)

admin.site.register(CodeUserStatus, CodeUserStatusAdmin)

admin.site.register(CodeQuestion,CodeQuestionAdmin)
