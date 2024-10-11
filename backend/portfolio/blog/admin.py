from django.contrib import admin
from .models import BlogPost, Tag, Category


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'category']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    save_on_top = True
    search_fields = ['title', 'content']
    exclude = ['thumbnail']


admin.site.register(Tag, TagAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Category)
