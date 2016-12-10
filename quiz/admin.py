from django.contrib import admin

from .models import  Question,Choice
# Register your models here.
from .models import Mark

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Code', {'fields': ['code_text'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question,QuestionAdmin)
admin.site.register(Mark)
#admin.site.register(Answer,answer)