from django.contrib import admin
from .models import Source, Article

class ArticleAdmin(admin.ModelAdmin):
  list_display = ["id", "title", "body", "author", "source", "url", "archived"]
#
# class SourceAdmin(admin.ModelAdmin):


admin.site.register(Source)
admin.site.register(Article)
