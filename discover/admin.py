from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('slug', 'author', 'publish')
    list_filter = ('created', 'publish', 'author')
    search_fields = ('body',)
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['publish']
admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
admin.site.register(Comment, CommentAdmin)
