from django.contrib import admin

from .models import Portfolio
from .models_project import (
    Project,
    SkillCategory,
    Skill,
    Experience,
    Education,
    ContactInfo,
)


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "theme", "visibility", "is_default", "created_at")
    list_filter = ("visibility", "is_default", "theme", "created_at")
    search_fields = ("title", "owner__username", "owner__email", "custom_domain")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at", "last_published_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        ("Informations", {
            "fields": ("owner", "title", "slug", "subtitle", "theme"),
        }),
        ("Publication", {
            "fields": ("visibility", "is_default", "custom_domain", "last_published_at"),
        }),
        ("Meta", {
            "fields": ("created_at", "updated_at"),
        }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "portfolio", "highlight", "is_visible", "sort_order")
    list_filter = ("highlight", "is_visible", "portfolio")
    search_fields = ("title", "portfolio__title", "tech_stack")
    autocomplete_fields = ("portfolio", "cover_image")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("portfolio", "sort_order")

    fieldsets = (
        (None, {
            "fields": ("portfolio", "title", "slug", "short_description", "description"),
        }),
        ("Liens", {
            "fields": ("github_url", "live_url"),
        }),
        ("Tech & visuel", {
            "fields": ("tech_stack", "cover_image", "highlight", "is_visible", "sort_order"),
        }),
        ("Meta", {
            "fields": ("created_at", "updated_at"),
        }),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "sort_order")
    ordering = ("sort_order", "name")
    search_fields = ("name",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "portfolio", "category", "level", "is_visible", "sort_order")
    list_filter = ("portfolio", "category", "is_visible")
    search_fields = ("name", "portfolio__title")
    ordering = ("portfolio", "sort_order", "name")
    autocomplete_fields = ("portfolio", "category")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "portfolio", "start_date", "end_date", "is_current")
    list_filter = ("portfolio", "company", "is_current")
    search_fields = ("role", "company", "portfolio__title")
    date_hierarchy = "start_date"
    ordering = ("portfolio", "-start_date")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("school", "degree", "portfolio", "start_date", "end_date")
    list_filter = ("portfolio", "school")
    search_fields = ("school", "degree", "portfolio__title")
    date_hierarchy = "start_date"
    ordering = ("portfolio", "-start_date")


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("portfolio", "email", "phone", "city", "country", "show_contact_form")
    search_fields = ("portfolio__title", "email", "city", "country")
    autocomplete_fields = ("portfolio",)
