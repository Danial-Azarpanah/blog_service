from django.contrib import admin

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "parent")
    search_fields = ("title",)
    ordering = ("parent__title",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "show_image", "author", "jalali_date")
    search_fields = ("title", "category__title", "author")
    list_filter = ("date_created",)
    prepopulated_fields = {"slug": ("title",)}

