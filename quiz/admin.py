from django.contrib import admin
from .models import  Question,Choice#,Status

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Code and Image', {'fields': ['code','image'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    

admin.site.register(Question,QuestionAdmin)
#admin.site.register(Question)