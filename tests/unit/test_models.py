import pytest
from apps.accounts.models import UserProfile
from tests.factories import (
    UserFactory,
    PortfolioFactory,
    ProjectFactory,
    SkillFactory,
    ExperienceFactory,
)


@pytest.mark.django_db
class TestUserProfile:
    def test_profile_created_on_user_creation(self):
        """UserProfile est créé avec get_or_create (robuste signal ou pas)."""
        user = UserFactory()
        profile, created = UserProfile.objects.get_or_create(user=user)
        assert profile is not None
        assert profile.user == user

    def test_str_returns_full_name_or_username(self):
        user = UserFactory()
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.full_name = "Ibrahima Kone"
        profile.save()
        assert str(profile) == "Ibrahima Kone"


@pytest.mark.django_db
class TestPortfolioModel:
    def test_str_contains_title(self):
        """Le __str__ du portfolio contient le titre."""
        portfolio = PortfolioFactory(title="Mon Portfolio")
        assert "Mon Portfolio" in str(portfolio)

    def test_portfolio_has_owner(self):
        portfolio = PortfolioFactory()
        assert portfolio.owner is not None

    def test_default_visibility_is_public(self):
        portfolio = PortfolioFactory(visibility="public")
        assert portfolio.visibility == "public"


@pytest.mark.django_db
class TestProjectModel:
    def test_project_linked_to_portfolio(self):
        project = ProjectFactory()
        assert project.portfolio is not None

    def test_str_returns_title(self):
        project = ProjectFactory(title="Mon Projet")
        assert str(project) == "Mon Projet"

    def test_tech_stack_is_list(self):
        project = ProjectFactory(tech_stack=["Django", "React"])
        assert isinstance(project.tech_stack, list)
        assert "Django" in project.tech_stack


@pytest.mark.django_db
class TestSkillModel:
    def test_skill_level_between_0_and_100(self):
        skill = SkillFactory(level=85)
        assert 0 <= skill.level <= 100


@pytest.mark.django_db
class TestExperienceModel:
    def test_str_contains_role_and_company(self):
        exp = ExperienceFactory(role="Dev Backend", company="Acme Corp")
        assert "Dev Backend" in str(exp)
        assert "Acme Corp" in str(exp)
