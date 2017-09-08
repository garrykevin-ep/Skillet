from django.contrib import admin

from .models import *


class MultiChoiceInline(admin.TabularInline):
    model = MultiChoice
    extra = 4

class FillChoiceInline(admin.TabularInline):
    model = FillChoice
    extra = 4

class MultiAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Code and Image', {'fields': ['code','image'], 'classes': ['collapse']}),
    ]
    inlines = [MultiChoiceInline]


class FillAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Code and Image', {'fields': ['code','image'], 'classes': ['collapse']}),
    ]
    inlines = [FillChoiceInline]

    def save_model(self, request, obj, form, change):
        obj.type = 'fill'
        obj.save()

admin.site.register(MultiQuestion,MultiAdmin)
admin.site.register(FillQuestion,FillAdmin)