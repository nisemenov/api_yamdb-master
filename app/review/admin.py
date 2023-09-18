from django.contrib import admin
from review.models import Review, Category, Title, Genre, Comment


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "score")
    search_fields = ("text",)
    list_filter = ('pub_date',)
    ordering = ('pk',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    ordering = ('pk',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category',)
    search_fields = ('name',)
    ordering = ('pk',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    ordering = ('pk',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    ordering = ('pk',)


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    ordering = ('pk',)


admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Comment, CommentAdmin)
