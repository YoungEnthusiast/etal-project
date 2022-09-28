from django.contrib import admin
from .models import Note

class NoteAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    # list_filter = ['status']
    # list_display_links = ['email']
    list_per_page = 100

admin.site.register(Note, NoteAdmin)
