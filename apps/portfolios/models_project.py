from django.db import models
from apps.portfolios.models import Portfolio
from apps.media.models import MediaFile  # on va le définir plus bas


class Project(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    tech_stack = models.JSONField(
        default=list,
        blank=True,
        help_text="Liste de technologies ex: ['Django', 'React']",
    )

    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)

    cover_image = models.ForeignKey(
        "media.MediaFile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="project_covers",
    )

    highlight = models.BooleanField(
        default=False,
        help_text="Afficher en priorité sur le portfolio.",
    )

    sort_order = models.PositiveIntegerField(default=1)
    is_visible = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        unique_together = ("portfolio", "slug")

    def __str__(self) -> str:
        return self.title

class SkillCategory(models.Model):
    name = models.CharField(max_length=100)
    sort_order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self) -> str:
        return self.name


class Skill(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="skills",
    )
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="skills",
    )
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField(
        default=70,
        help_text="Niveau (0-100) pour une barre de progression.",
    )
    sort_order = models.PositiveIntegerField(default=1)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]
        unique_together = ("portfolio", "name")

    def __str__(self) -> str:
        return self.name

class Experience(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["sort_order", "-start_date"]

    def __str__(self) -> str:
        return f"{self.role} @ {self.company}"


class Education(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="educations",
    )
    school = models.CharField(max_length=150)
    degree = models.CharField(max_length=150, blank=True)
    field_of_study = models.CharField(max_length=150, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["sort_order", "-start_date"]

    def __str__(self) -> str:
        return f"{self.school} — {self.degree or self.field_of_study}"

class ContactInfo(models.Model):
    portfolio = models.OneToOneField(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="contact_info",
    )
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    show_contact_form = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Informations de contact"
        verbose_name_plural = "Informations de contact"

    def __str__(self) -> str:
        return f"Contact de {self.portfolio}"
