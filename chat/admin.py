from django.contrib import admin
from .models import ChatNotification

# Register your models here.


class ChatNotificationAdmin(admin.ModelAdmin):
    list_display = ['created', 'owner', 'message', 'unreads']
    search_fields = ['owner', 'message']
    # list_filter = ['status']
    # list_display_links = ['email']
    list_per_page = 100

admin.site.register(ChatNotification, ChatNotificationAdmin)
