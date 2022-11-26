from django.contrib import admin

from .models import Category, Genre, Title


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "year", "description", "category")
    list_filter = ("category", "year")
    search_fields = ("name",)
