from django.contrib import admin
from .models import Question, Response

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'author', 'title']
    # search_fields = ['owner', 'message']
    # list_filter = ['status']
    # list_display_links = ['email']
    list_per_page = 100

admin.site.register(Question, QuestionAdmin)

class ResponseAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'user', 'question']
    # search_fields = ['owner', 'message']
    # list_filter = ['status']
    # list_display_links = ['email']
    list_per_page = 100

admin.site.register(Response, ResponseAdmin)
