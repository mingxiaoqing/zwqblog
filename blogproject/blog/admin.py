from django.contrib import admin
from .models import Article,Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','created_time','modified_time','category','author']

admin.site.register(Article,ArticleAdmin)
admin.site.register(Category)




