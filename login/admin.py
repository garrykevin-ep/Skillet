from django.contrib import admin

from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    '''
        Admin View for UserProfile
    '''
    list_display = ('get_name','user','mark')
    def get_name(self, obj):
    	return obj.user.id
    get_name.admin_order_field = 'id'
    get_name.short_description = 'id'

admin.site.register(UserProfile, UserProfileAdmin)
