import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="strongpass123",
    )


@pytest.fixture
def auth_client(api_client, user):
    """Client authentifié avec JWT."""
    response = api_client.post(
        "/api/auth/token/",
        {"username": "testuser", "password": "strongpass123"},
        format="json",
    )
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client
