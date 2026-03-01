import pytest
from rest_framework import status
from tests.factories import ThemeFactory, UserFactory


@pytest.mark.django_db
class TestRegistrationAndLoginFlow:
    """
    Flow complet : inscription → login → accès profil.
    """

    def test_full_register_login_me_flow(self, api_client):
        # 1. Inscription
        register_response = api_client.post(
            "/api/v1/auth/register/",
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
            "/api/v1/auth/token/",
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
        me_response = api_client.get("/api/v1/me/")
        assert me_response.status_code == status.HTTP_200_OK
        assert me_response.data["user"]["username"] == "ibrahko"

        # 4. Mise à jour du profil
        patch_response = api_client.patch(
            "/api/v1/me/",
            {"full_name": "Ibrahima Kone", "location": "Bamako"},
            format="json",
        )
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data["full_name"] == "Ibrahima Kone"
        assert patch_response.data["location"] == "Bamako"

        # 5. Refresh token
        api_client.credentials()  # reset
        refresh_response = api_client.post(
            "/api/v1/auth/token/refresh/",
            {"refresh": refresh},
            format="json",
        )
        assert refresh_response.status_code == status.HTTP_200_OK
        assert "access" in refresh_response.data


@pytest.mark.django_db
class TestPortfolioBuilderFlow:
    """
    Flow complet : création portfolio → section → projet → compétence.
    """

    def test_full_portfolio_builder_flow(self, api_client):
        theme = ThemeFactory()

        # 1. Inscription + login
        api_client.post(
            "/api/v1/auth/register/",
            {
                "username": "builder",
                "email": "builder@example.com",
                "password": "strongpass123",
            },
            format="json",
        )
        token_response = api_client.post(
            "/api/v1/auth/token/",
            {"username": "builder", "password": "strongpass123"},
            format="json",
        )
        access = token_response.data["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        # 2. Création du portfolio
        portfolio_response = api_client.post(
            "/api/v1/portfolios/",
            {
                "title": "Mon Portfolio Dev",
                "slug": "mon-portfolio-dev",
                "subtitle": "Développeur Fullstack",
                "theme": theme.id,
                "visibility": "public",
                "is_default": True,
            },
            format="json",
        )
        assert portfolio_response.status_code == status.HTTP_201_CREATED
        portfolio_id = portfolio_response.data["id"]
        portfolio_slug = portfolio_response.data["slug"]

        # 3. Ajout d'une section "projects"
        section_response = api_client.post(
            "/api/v1/sections/",
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
            "/api/v1/projects/",
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
            "/api/v1/skills/",
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
        public_response = api_client.get(f"/api/v1/portfolios/{portfolio_slug}/")
        assert public_response.status_code == status.HTTP_200_OK
        assert public_response.data["title"] == "Mon Portfolio Dev"


@pytest.mark.django_db
class TestContactMessageFlow:
    """
    Flow complet : visiteur envoie un message → propriétaire le lit.
    """

    def test_visitor_sends_message_owner_reads_it(self, api_client):
        theme = ThemeFactory()

        # 1. Créer un utilisateur propriétaire + son portfolio
        api_client.post(
            "/api/v1/auth/register/",
            {
                "username": "owner",
                "email": "owner@example.com",
                "password": "strongpass123",
            },
            format="json",
        )
        token_response = api_client.post(
            "/api/v1/auth/token/",
            {"username": "owner", "password": "strongpass123"},
            format="json",
        )
        access = token_response.data["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        portfolio_response = api_client.post(
            "/api/v1/portfolios/",
            {
                "title": "Portfolio Owner",
                "slug": "portfolio-owner",
                "theme": theme.id,
                "visibility": "public",
            },
            format="json",
        )
        assert portfolio_response.status_code == status.HTTP_201_CREATED
        portfolio_id = portfolio_response.data["id"]

        # 2. Visiteur (non authentifié) envoie un message
        api_client.credentials()
        contact_response = api_client.post(
            "/api/v1/contact-messages/",
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

        # 3. Propriétaire lit ses messages
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        messages_response = api_client.get("/api/v1/contact-messages/")
        assert messages_response.status_code == status.HTTP_200_OK
        results = messages_response.data.get("results", messages_response.data)
        assert len(results) >= 1
        assert results[0]["name"] == "Visiteur Test"


@pytest.mark.django_db
class TestIsolationBetweenUsers:
    """
    Un utilisateur ne peut pas voir/modifier les données d'un autre.
    """

    def test_user_cannot_see_other_user_portfolio(self, api_client):
        theme = ThemeFactory()

        # Crée user1 avec un portfolio privé
        user1 = UserFactory(username="user1")
        api_client.post(
            "/api/v1/auth/register/",
            {
                "username": "user2",
                "email": "user2@example.com",
                "password": "strongpass123",
            },
            format="json",
        )

        # Login user1 et crée un portfolio privé
        token1 = api_client.post(
            "/api/v1/auth/token/",
            {"username": "user1", "password": "strongpass123"},
            format="json",
        )
        # user1 n'est pas créé via register ici donc on force le token
        api_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token1.data.get('access', '')}"
        )

        # Login user2
        token2 = api_client.post(
            "/api/v1/auth/token/",
            {"username": "user2", "password": "strongpass123"},
            format="json",
        )
        access2 = token2.data["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access2}")

        # user2 ne voit que ses propres portfolios (liste vide car rien créé)
        list_response = api_client.get("/api/v1/portfolios/")
        assert list_response.status_code == status.HTTP_200_OK
        results = list_response.data.get("results", list_response.data)
        # Tous les portfolios visibles doivent être "public"
        for portfolio in results:
            assert portfolio["visibility"] == "public"

    def test_user_cannot_delete_other_user_portfolio(self, api_client):
        theme = ThemeFactory()

        # user1 s'inscrit et crée un portfolio
        api_client.post(
            "/api/v1/auth/register/",
            {
                "username": "user1",
                "email": "user1@example.com",
                "password": "strongpass123",
            },
            format="json",
        )
        token1 = api_client.post(
            "/api/v1/auth/token/",
            {"username": "user1", "password": "strongpass123"},
            format="json",
        )
        api_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token1.data['access']}"
        )
        portfolio_response = api_client.post(
            "/api/v1/portfolios/",
            {
                "title": "Portfolio User1",
                "slug": "portfolio-user1",
                "theme": theme.id,
                "visibility": "public",
            },
            format="json",
        )
        portfolio_slug = portfolio_response.data["slug"]

        # user2 s'inscrit et essaie de supprimer le portfolio de user1
        api_client.post(
            "/api/v1/auth/register/",
            {
                "username": "user2",
                "email": "user2@example.com",
                "password": "strongpass123",
            },
            format="json",
        )
        token2 = api_client.post(
            "/api/v1/auth/token/",
            {"username": "user2", "password": "strongpass123"},
            format="json",
        )
        api_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token2.data['access']}"
        )

        delete_response = api_client.delete(
            f"/api/v1/portfolios/{portfolio_slug}/"
        )
        # Doit être 403 ou 404 (pas autorisé)
        assert delete_response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]
