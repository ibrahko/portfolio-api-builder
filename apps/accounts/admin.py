from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "headline", "location", "created_at")
    search_fields = ("user__username", "user__email", "full_name", "headline")
    list_filter = ("created_at",)
    autocomplete_fields = ("user",)
