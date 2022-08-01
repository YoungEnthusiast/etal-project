from django.contrib import admin
from .models import Researcher
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
                    'fields': ('type', 'affiliation_name', 'affiliation_address', 'city', 'state', 'country')
                }
            )
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'type', 'affiliation_name', 'affiliation_address', 'city', 'state', 'country')}
        ),
    )
admin.site.register(Researcher, ResearcherAdmin)
