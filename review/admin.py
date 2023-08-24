from django.contrib import admin
from .models import Review, Category, Title, Genre


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "score")
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-empty-"


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category', 'genre')
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
