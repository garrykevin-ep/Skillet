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
	inlines = [TestCaseInline,ExtendInline]
	def save_model(self, request, obj, form, change):
		obj.type = 'code'
		obj.save()

admin.site.register(CodeQuestion,CodeQuestionAdmin)
