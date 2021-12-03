from django.contrib import admin
from .models import Profile, FriendRequest
# Register your models here.
class ProfileListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user',]
    
    class Meta:
        model = Profile
admin.site.register(Profile, ProfileListAdmin)
admin.site.register(FriendRequest)