from accounts.models import Profile
from django.contrib import admin

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'active')

admin.site.register(Profile, ProfileAdmin)