from django.contrib import admin

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "full_name", "is_active", "jalali_date")
    list_filter = ("is_active", "is_admin")
    search_fields = ("phone_number", "full_name")
    ordering = ("is_admin", "-date_joined")
