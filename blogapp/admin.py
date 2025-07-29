from django.contrib import admin
from .models import *
from .const import *

class ArticleAdmin(admin.ModelAdmin):
  list_display = ("title", "content", "author", "category", "status", "order", "created_at")
  search_fields = ["title"]
  list_filter = ("title", "created_at")
  prepopulated_fields = {"slug": ("title",)}    

class CategoryAdmin(admin.ModelAdmin):
  list_display = ("title", "description", "order")
  search_fields = ["title"]
  list_filter = ("title", "order")
  prepopulated_fields = {"slug": ("title",)}

class CommentAdmin(admin.ModelAdmin):
  list_display = ("user", "article", "content")
  search_fields = ["content"]
  list_filter = ("user", "article")

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.site_header = ADMIN_PAGE_HEADER
admin.site.site_title = ADMIN_PAGE_TITLE
