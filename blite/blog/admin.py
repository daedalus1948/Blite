from django.contrib import admin
from .models import Post

class AdminPost(admin.ModelAdmin):

    list_display = ['title', 'create_date', 'published', 'author']
    list_filter = ['create_date']

    class Meta:
        model = Post

admin.site.register(Post, AdminPost)
    