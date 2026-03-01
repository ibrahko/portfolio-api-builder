import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

from apps.accounts.models import UserProfile
from apps.themes.models import Theme
from apps.portfolios.models import Portfolio
from apps.portfolios.models_project import (
    Project,
    Skill,
    SkillCategory,
    Experience,
    Education,
)
from apps.sections.models import Section
from apps.notifications.models import ContactMessage

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "strongpass123")


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    full_name = factory.Faker("name", locale="fr_FR")
    headline = factory.Faker("job", locale="fr_FR")
    bio = factory.Faker("paragraph", locale="fr_FR")
    location = "Bamako, Mali"


class ThemeFactory(DjangoModelFactory):
    class Meta:
        model = Theme

    name = factory.Sequence(lambda n: f"Theme {n}")
    slug = factory.Sequence(lambda n: f"theme-{n}")
    is_active = True


class PortfolioFactory(DjangoModelFactory):
    class Meta:
        model = Portfolio

    owner = factory.SubFactory(UserFactory)
    theme = factory.SubFactory(ThemeFactory)
    title = factory.Sequence(lambda n: f"Portfolio {n}")
    slug = factory.Sequence(lambda n: f"portfolio-{n}")
    visibility = "public"


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    portfolio = factory.SubFactory(PortfolioFactory)
    title = factory.Sequence(lambda n: f"Project {n}")
    slug = factory.Sequence(lambda n: f"project-{n}")
    short_description = factory.Faker("sentence")
    tech_stack = ["Django", "React"]
    is_visible = True


class SkillCategoryFactory(DjangoModelFactory):
    class Meta:
        model = SkillCategory

    name = factory.Sequence(lambda n: f"Category {n}")


class SkillFactory(DjangoModelFactory):
    class Meta:
        model = Skill

    portfolio = factory.SubFactory(PortfolioFactory)
    category = factory.SubFactory(SkillCategoryFactory)
    name = factory.Sequence(lambda n: f"Skill {n}")
    level = 80
    is_visible = True


class ExperienceFactory(DjangoModelFactory):
    class Meta:
        model = Experience

    portfolio = factory.SubFactory(PortfolioFactory)
    role = factory.Faker("job", locale="fr_FR")
    company = factory.Faker("company", locale="fr_FR")
    start_date = factory.Faker("date_between", start_date="-5y", end_date="-1y")
    end_date = factory.Faker("date_between", start_date="-1y", end_date="today")
    is_current = False


class SectionFactory(DjangoModelFactory):
    class Meta:
        model = Section

    portfolio = factory.SubFactory(PortfolioFactory)
    type = "projects"
    title = factory.Sequence(lambda n: f"Section {n}")
    slug = factory.Sequence(lambda n: f"section-{n}")
    order = factory.Sequence(lambda n: n)
    settings = {}


class ContactMessageFactory(DjangoModelFactory):
    class Meta:
        model = ContactMessage

    portfolio = factory.SubFactory(PortfolioFactory)
    name = factory.Faker("name", locale="fr_FR")
    email = factory.Faker("email")
    subject = factory.Faker("sentence")
    message = factory.Faker("paragraph")
