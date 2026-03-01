import pytest
from django.contrib.auth import get_user_model

from apps.accounts.serializers import RegisterSerializer

User = get_user_model()


@pytest.mark.django_db
class TestRegisterSerializer:
    def test_valid_data_creates_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "strongpass123",
        }
        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()
        assert user.pk is not None
        assert user.check_password("strongpass123")

    def test_duplicate_username_raises_error(self):
        User.objects.create_user(username="existing", email="a@a.com", password="pass1234")
        data = {
            "username": "existing",
            "email": "other@example.com",
            "password": "strongpass123",
        }
        serializer = RegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "username" in serializer.errors

    def test_duplicate_email_raises_error(self):
        User.objects.create_user(username="user1", email="same@example.com", password="pass1234")
        data = {
            "username": "user2",
            "email": "same@example.com",
            "password": "strongpass123",
        }
        serializer = RegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_short_password_raises_error(self):
        data = {
            "username": "user3",
            "email": "user3@example.com",
            "password": "short",
        }
        serializer = RegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors
