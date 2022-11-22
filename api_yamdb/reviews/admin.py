from django.contrib import admin

from .models import Categories, Genres, Titles, GenreTitles


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Titles)
class TitlesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "year", "rating", "description", "category")
    list_filter = ("rating", "category", "year")
    search_fields = ("name",)


@admin.register(GenreTitles)
class GenreTitles(admin.ModelAdmin):
    list_display = ("id", "title", "genre")
