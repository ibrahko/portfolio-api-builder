import pytest
from django.urls import reverse
from rest_framework import status
from tests.factories import UserFactory


@pytest.mark.django_db
class TestRegisterEndpoint:
    url = "/api/auth/register/"

    def test_register_success(self, api_client):
        data = {
            "username": "ibrahko",
            "email": "ibrahko@example.com",
            "password": "strongpass123",
        }
        response = api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert "user" in response.data
        assert "profile" in response.data
        assert response.data["user"]["username"] == "ibrahko"

    def test_register_duplicate_username(self, api_client):
        UserFactory(username="ibrahko")
        data = {
            "username": "ibrahko",
            "email": "other@example.com",
            "password": "strongpass123",
        }
        response = api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_weak_password(self, api_client):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "123",
        }
        response = api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestTokenEndpoint:
    url = "/api/auth/token/"

    def test_login_success(self, api_client):
        UserFactory(username="ibrahko", password="strongpass123")
        data = {"username": "ibrahko", "password": "strongpass123"}
        response = api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_wrong_password(self, api_client):
        UserFactory(username="ibrahko")
        data = {"username": "ibrahko", "password": "wrongpass"}
        response = api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestMeEndpoint:
    url = "/api/me/"

    def test_get_me_authenticated(self, auth_client):
        response = auth_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert "user" in response.data
        assert "profile" in response.data

    def test_get_me_unauthenticated(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_me_updates_profile(self, auth_client):
        data = {"full_name": "Ibrahima Kone", "location": "Bamako"}
        response = auth_client.patch(self.url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["full_name"] == "Ibrahima Kone"
