from django.contrib import admin

from .models import NotificationPreference, ContactMessage, EmailLog


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "receive_contact_emails", "receive_product_updates")
    search_fields = ("user__username", "user__email")
    autocomplete_fields = ("user",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("portfolio", "name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read", "created_at", "portfolio")
    search_fields = ("name", "email", "subject", "message", "portfolio__title")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    autocomplete_fields = ("portfolio",)


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ("to_email", "subject", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("to_email", "subject", "error_message")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ("to_email", "subject", "body_preview", "status", "error_message", "created_at", "meta")
