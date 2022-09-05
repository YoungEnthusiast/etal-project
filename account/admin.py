from django.contrib import admin
from .models import Researcher, Collab, Notification, Flag, Report, Stranger, CollabDoc
from .forms import CustomRegisterForm
# from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class ResearcherAdmin(UserAdmin):
    list_display = ['created', 'username', 'first_name', 'last_name', 'email', 'type', 'is_staff', 'is_superuser']
    list_display_links = ['username', 'first_name']
    search_fields = ['username']
    list_filter = ['is_staff', 'is_superuser', 'type']
    list_editable = ['is_staff', 'is_superuser']
    list_per_page = 100

    add_form = CustomRegisterForm
    fieldsets = (
            *UserAdmin.fieldsets,
            (
                "Custom Fields",
                {
                    'fields': ('type', 'photograph', 'affiliation_name', 'affiliation_address', 'bell_unreads', 'city', 'state', 'country')
                }
            )
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'type', 'photograph', 'affiliation_name', 'affiliation_address', 'bell_unreads', 'city', 'state', 'country')}
        ),
    )
admin.site.register(Researcher, ResearcherAdmin)

class CollabAdmin(admin.ModelAdmin):
    list_display = ['title', 'abstract']
    search_fields = ['title', 'abstract']
    # list_filter = ['status']
    # list_display_links = ['email']
    list_per_page = 100

admin.site.register(Collab, CollabAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['owner', 'message', 'unreads']
    search_fields = ['owner', 'message']
    # list_filter = ['status']
    # list_display_links = ['email']
    list_per_page = 100

admin.site.register(Notification, NotificationAdmin)

class FlagAdmin(admin.ModelAdmin):
    list_display = ['reason']
    search_fields = ['reason']
    # list_filter = ['status']
    # list_display_links = ['email']
    list_per_page = 100

admin.site.register(Flag, FlagAdmin)

class ReportAdmin(admin.ModelAdmin):
    list_display = ['complainer', 'collab', 'receiver']
    search_fields = []
    # list_filter = ['status']
    # list_display_links = ['email']
    list_per_page = 100

admin.site.register(Report, ReportAdmin)

class StrangerAdmin(admin.ModelAdmin):
    list_display = ['first_username']
    search_fields = []
    # list_filter = ['status']
    # list_display_links = ['email']
    list_per_page = 100

admin.site.register(Stranger, StrangerAdmin)
class CollabDocAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'document']
    search_fields = []
    # list_filter = ['status']
    # list_display_links = ['email']
    list_per_page = 100

admin.site.register(CollabDoc, CollabDocAdmin)
