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
        (None,               {'fields': ['test','question_text']}),
        ('Code and Image', {'fields': ['code','image'], 'classes': ['collapse']}),
    ]
    inlines = [MultiChoiceInline]


class FillAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['test','question_text']}),
        ('Code and Image', {'fields': ['code','image'], 'classes': ['collapse']}),
    ]
    inlines = [FillChoiceInline]

    def save_model(self, request, obj, form, change):
        obj.type = 'fill'
        obj.save()

class TestStatusAdmin(admin.ModelAdmin):
    '''
        Admin View for TestStatus
    '''
    list_display = ('user','test','mark','minute')
    list_filter = ('test',)
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('use',)

admin.site.register(TestStatus, TestStatusAdmin)

admin.site.register(MultiQuestion,MultiAdmin)
admin.site.register(FillQuestion,FillAdmin)
admin.site.register(Test)