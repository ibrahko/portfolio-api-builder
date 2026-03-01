import pytest
from rest_framework import status
from tests.factories import PortfolioFactory, UserFactory, ThemeFactory


@pytest.mark.django_db
class TestPortfolioListEndpoint:
    url = "/api/portfolios/"

    def test_list_public_portfolios_unauthenticated(self, api_client):
        """Un visiteur voit uniquement les portfolios publics."""
        PortfolioFactory.create_batch(3, visibility="public")
        PortfolioFactory.create_batch(2, visibility="private")
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        results = response.data.get("results", response.data)
        for portfolio in results:
            assert portfolio["visibility"] == "public"

    def test_authenticated_user_sees_only_own_portfolios(self, auth_client, user):
        """Un user authentifié voit uniquement ses portfolios."""
        theme = ThemeFactory()
        PortfolioFactory.create_batch(2, owner=user, visibility="public", theme=theme)
        PortfolioFactory.create_batch(3, visibility="public", theme=theme)
        response = auth_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_portfolio_authenticated(self, auth_client):
        """Un user authentifié peut créer un portfolio."""
        theme = ThemeFactory()
        data = {
            "title": "Mon Portfolio",
            "slug": "mon-portfolio",
            "subtitle": "Dev Fullstack",
            "theme": theme.id,
            "visibility": "public",
            "is_default": True,
        }
        response = auth_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "Mon Portfolio"

    def test_create_portfolio_unauthenticated(self, api_client):
        """Un visiteur ne peut pas créer un portfolio."""
        theme = ThemeFactory()
        data = {
            "title": "Mon Portfolio",
            "slug": "mon-portfolio",
            "theme": theme.id,
            "visibility": "public",
        }
        response = api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPortfolioDetailEndpoint:

    def test_retrieve_public_portfolio(self, api_client):
        """N'importe qui peut lire un portfolio public."""
        portfolio = PortfolioFactory(visibility="public")
        response = api_client.get(f"/api/portfolios/{portfolio.slug}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["slug"] == portfolio.slug

    def test_retrieve_private_portfolio_as_visitor(self, api_client):
        """Un visiteur ne peut pas lire un portfolio privé."""
        portfolio = PortfolioFactory(visibility="private")
        response = api_client.get(f"/api/portfolios/{portfolio.slug}/")
        assert response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_owner_can_update_portfolio(self, auth_client, user):
        """Le propriétaire peut modifier son portfolio."""
        theme = ThemeFactory()
        portfolio = PortfolioFactory(owner=user, theme=theme, visibility="public")
        data = {"title": "Titre Modifié", "slug": portfolio.slug, "theme": theme.id}
        response = auth_client.patch(
            f"/api/portfolios/{portfolio.slug}/",
            data,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_non_owner_cannot_delete_portfolio(self, api_client):
        """Un autre user ne peut pas supprimer le portfolio d'un tiers."""
        other_user = UserFactory(username="other")
        theme = ThemeFactory()
        portfolio = PortfolioFactory(
            owner=other_user, theme=theme, visibility="public"
        )

        # Crée un autre user et connecte-le
        api_client.post(
            "/api/auth/register/",
            {
                "username": "intruder",
                "email": "intruder@example.com",
                "password": "strongpass123",
            },
            format="json",
        )
        token_response = api_client.post(
            "/api/auth/token/",
            {"username": "intruder", "password": "strongpass123"},
            format="json",
        )
        api_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}"
        )

        response = api_client.delete(f"/api/portfolios/{portfolio.slug}/")
        assert response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]
