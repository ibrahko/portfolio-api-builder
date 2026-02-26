from rest_framework import serializers

from apps.themes.serializers import ThemeSerializer
from apps.themes.models import Theme
from apps.portfolios.models import Portfolio
from apps.portfolios.models_project import (
    Project,
    SkillCategory,
    Skill,
    Experience,
    Education,
    ContactInfo,
)
from apps.sections.models import Section

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "tech_stack",
            "github_url",
            "live_url",
            "cover_image",
            "highlight",
            "is_visible",
            "sort_order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")


class SkillCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillCategory
        fields = ["id", "name", "sort_order"]


class SkillSerializer(serializers.ModelSerializer):
    category = SkillCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=SkillCategory.objects.all(),
        source="category",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Skill
        fields = [
            "id",
            "name",
            "level",
            "is_visible",
            "sort_order",
            "category",
            "category_id",
        ]


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            "id",
            "role",
            "company",
            "location",
            "start_date",
            "end_date",
            "is_current",
            "description",
            "sort_order",
        ]


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            "id",
            "school",
            "degree",
            "field_of_study",
            "start_date",
            "end_date",
            "description",
            "sort_order",
        ]


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = [
            "email",
            "phone",
            "city",
            "country",
            "show_contact_form",
        ]


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = [
            "id",
            "type",
            "title",
            "slug",
            "is_visible",
            "order",
            "settings",
        ]

class PortfolioDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    theme = ThemeSerializer(read_only=True)

    sections = SectionSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    contact_info = ContactInfoSerializer(read_only=True)

    class Meta:
        model = Portfolio
        fields = [
            "id",
            "title",
            "slug",
            "subtitle",
            "owner_username",
            "theme",
            "visibility",
            "custom_domain",
            "is_default",
            "sections",
            "projects",
            "skills",
            "experiences",
            "educations",
            "contact_info",
            "created_at",
            "updated_at",
            "last_published_at",
        ]
        read_only_fields = (
            "id",
            "owner_username",
            "created_at",
            "updated_at",
            "last_published_at",
        )


class PortfolioListSerializer(serializers.ModelSerializer):
    theme = ThemeSerializer(read_only=True)

    class Meta:
        model = Portfolio
        fields = [
            "id",
            "title",
            "slug",
            "subtitle",
            "theme",
            "visibility",
            "is_default",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")


class PortfolioWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = [
            "title",
            "slug",
            "subtitle",
            "theme",
            "visibility",
            "custom_domain",
            "is_default",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        return Portfolio.objects.create(owner=user, **validated_data)

class PortfolioListSerializer(serializers.ModelSerializer):
    theme = ThemeSerializer(read_only=True)

    class Meta:
        model = Portfolio
        fields = [
            "id",
            "title",
            "slug",
            "subtitle",
            "theme",
            "visibility",
            "is_default",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")


class PortfolioWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = [
            "title",
            "slug",
            "subtitle",
            "theme",
            "visibility",
            "custom_domain",
            "is_default",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        return Portfolio.objects.create(owner=user, **validated_data)

