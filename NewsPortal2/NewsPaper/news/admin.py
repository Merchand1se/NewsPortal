from django.contrib import admin
from .models import Post, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'creationDate', )
    list_filter = ('title', 'creationDate', 'postCategory', 'type')
    search_fields = ('title', 'postCategory',)

    def get_absolute_url(self):
        return f'/post/{self.id}'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def get_absolute_url(self):
        return f'/category/{self.id}'



admin.site.register(Post, PostAdmin)
admin.site.register(Category)

