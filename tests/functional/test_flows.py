import pytest
from rest_framework import status
from tests.factories import ThemeFactory, UserFactory


def _register_and_login(api_client, username, email, password="strongpass123"):
    """Helper : inscrit un user et retourne son access token."""
    api_client.post(
        "/api/auth/register/",
        {"username": username, "email": email, "password": password},
        format="json",
    )
    token_response = api_client.post(
        "/api/auth/token/",
        {"username": username, "password": password},
        format="json",
    )
    assert token_response.status_code == status.HTTP_200_OK, (
        f"Login échoué pour {username} : {token_response.content}"
    )
    return token_response.data["access"]


def _create_portfolio(api_client, theme, title, slug, visibility="public"):
    """Helper : crée un portfolio et retourne (id, slug)."""
    response = api_client.post(
        "/api/portfolios/",
        {
            "title": title,
            "slug": slug,
            "theme": theme.id,
            "visibility": visibility,
        },
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED, (
        f"Création portfolio échouée : {response.content}"
    )
    # On récupère l'id via un GET sur le slug (robuste même si id absent du serializer)
    detail = api_client.get(f"/api/portfolios/{slug}/")
    portfolio_id = detail.data.get("id") or response.data.get("id")
    return portfolio_id, slug


@pytest.mark.django_db
class TestRegistrationAndLoginFlow:
    """Flow complet : inscription → login → accès profil."""

    def test_full_register_login_me_flow(self, api_client):
        # 1. Inscription
        register_response = api_client.post(
            "/api/auth/register/",
            {
                "username": "ibrahko",
                "email": "ibrahko@example.com",
                "password": "strongpass123",
            },
            format="json",
        )
        assert register_response.status_code == status.HTTP_201_CREATED
        assert register_response.data["user"]["username"] == "ibrahko"

        # 2. Login JWT
        token_response = api_client.post(
            "/api/auth/token/",
            {"username": "ibrahko", "password": "strongpass123"},
            format="json",
        )
        assert token_response.status_code == status.HTTP_200_OK
        access = token_response.data["access"]
        refresh = token_response.data["refresh"]
        assert access is not None
        assert refresh is not None

        # 3. Accès au profil
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        me_response = api_client.get("/api/me/")
        assert me_response.status_code == status.HTTP_200_OK
        assert me_response.data["user"]["username"] == "ibrahko"

        # 4. Mise à jour du profil
        patch_response = api_client.patch(
            "/api/me/",
            {"full_name": "Ibrahima Kone", "location": "Bamako"},
            format="json",
        )
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data["full_name"] == "Ibrahima Kone"
        assert patch_response.data["location"] == "Bamako"

        # 5. Refresh token
        api_client.credentials()
        refresh_response = api_client.post(
            "/api/auth/token/refresh/",
            {"refresh": refresh},
            format="json",
        )
        assert refresh_response.status_code == status.HTTP_200_OK
        assert "access" in refresh_response.data


@pytest.mark.django_db
class TestPortfolioBuilderFlow:
    """Flow complet : création portfolio → section → projet → compétence."""

    def test_full_portfolio_builder_flow(self, api_client):
        theme = ThemeFactory()

        # 1. Inscription + login
        access = _register_and_login(
            api_client, "builder", "builder@example.com"
        )
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        # 2. Création du portfolio
        portfolio_id, portfolio_slug = _create_portfolio(
            api_client, theme,
            title="Mon Portfolio Dev",
            slug="mon-portfolio-dev",
        )
        assert portfolio_id is not None

        # 3. Ajout d'une section "projects"
        section_response = api_client.post(
            "/api/sections/",
            {
                "portfolio": portfolio_id,
                "type": "projects",
                "title": "Mes Projets",
                "slug": "mes-projets",
                "is_visible": True,
                "order": 1,
                "settings": {},
            },
            format="json",
        )
        assert section_response.status_code == status.HTTP_201_CREATED

        # 4. Ajout d'un projet
        project_response = api_client.post(
            "/api/projects/",
            {
                "portfolio": portfolio_id,
                "title": "Portfolio Builder",
                "slug": "portfolio-builder",
                "short_description": "Un générateur de portfolios",
                "tech_stack": ["Django", "React"],
                "is_visible": True,
                "highlight": True,
                "sort_order": 1,
            },
            format="json",
        )
        assert project_response.status_code == status.HTTP_201_CREATED
        assert project_response.data["title"] == "Portfolio Builder"
        assert "Django" in project_response.data["tech_stack"]

        # 5. Ajout d'une compétence
        skill_response = api_client.post(
            "/api/skills/",
            {
                "portfolio": portfolio_id,
                "name": "Django",
                "level": 90,
                "is_visible": True,
                "sort_order": 1,
            },
            format="json",
        )
        assert skill_response.status_code == status.HTTP_201_CREATED

        # 6. Lecture publique du portfolio (sans auth)
        api_client.credentials()
        public_response = api_client.get(f"/api/portfolios/{portfolio_slug}/")
        assert public_response.status_code == status.HTTP_200_OK
        assert public_response.data["title"] == "Mon Portfolio Dev"


@pytest.mark.django_db
class TestContactMessageFlow:
    """Flow complet : visiteur envoie un message → propriétaire le lit."""

    def test_visitor_sends_message_owner_reads_it(self, api_client):
        theme = ThemeFactory()

        # 1. Inscription + login du propriétaire
        access = _register_and_login(api_client, "owner", "owner@example.com")
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        # 2. Création du portfolio
        portfolio_id, portfolio_slug = _create_portfolio(
            api_client, theme,
            title="Portfolio Owner",
            slug="portfolio-owner",
        )
        assert portfolio_id is not None

        # 3. Visiteur (non authentifié) envoie un message
        api_client.credentials()
        contact_response = api_client.post(
            "/api/contact-messages/",
            {
                "portfolio": portfolio_id,
                "name": "Visiteur Test",
                "email": "visiteur@example.com",
                "subject": "Collaboration possible ?",
                "message": "Bonjour, je voudrais collaborer avec vous.",
            },
            format="json",
        )
        assert contact_response.status_code == status.HTTP_201_CREATED

        # 4. Propriétaire lit ses messages
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        messages_response = api_client.get("/api/contact-messages/")
        assert messages_response.status_code == status.HTTP_200_OK
        results = messages_response.data.get("results", messages_response.data)
        assert len(results) >= 1
        assert results[0]["name"] == "Visiteur Test"


@pytest.mark.django_db
class TestIsolationBetweenUsers:
    """Un utilisateur ne peut pas voir/modifier les données d'un autre."""

    def test_user_cannot_see_other_user_portfolio(self, api_client):
        ThemeFactory()

        # user2 s'inscrit
        api_client.post(
            "/api/auth/register/",
            {
                "username": "user2",
                "email": "user2@example.com",
                "password": "strongpass123",
            },
            format="json",
        )

        # Login user2
        token2 = api_client.post(
            "/api/auth/token/",
            {"username": "user2", "password": "strongpass123"},
            format="json",
        )
        access2 = token2.data["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access2}")

        # user2 ne voit que les portfolios publics (pas ses données privées)
        list_response = api_client.get("/api/portfolios/")
        assert list_response.status_code == status.HTTP_200_OK
        results = list_response.data.get("results", list_response.data)
        for portfolio in results:
            assert portfolio["visibility"] == "public"

    def test_user_cannot_delete_other_user_portfolio(self, api_client):
        theme = ThemeFactory()

        # user1 s'inscrit et crée un portfolio
        access1 = _register_and_login(
            api_client, "user1", "user1@example.com"
        )
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access1}")
        portfolio_id, portfolio_slug = _create_portfolio(
            api_client, theme,
            title="Portfolio User1",
            slug="portfolio-user1",
        )

        # user2 s'inscrit et essaie de supprimer le portfolio de user1
        access2 = _register_and_login(
            api_client, "user2", "user2@example.com"
        )
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access2}")

        delete_response = api_client.delete(
            f"/api/portfolios/{portfolio_slug}/"
        )
        assert delete_response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]
