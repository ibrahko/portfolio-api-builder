import pytest
from unittest.mock import MagicMock
from shared.permissions import IsOwnerOrReadOnly, IsOwnerViaPortfolio


class TestIsOwnerOrReadOnly:
    def _make_request(self, method, user):
        request = MagicMock()
        request.method = method
        request.user = user
        return request

    def test_safe_method_public_object_allowed(self):
        perm = IsOwnerOrReadOnly()
        obj = MagicMock()
        obj.visibility = "public"
        request = self._make_request("GET", MagicMock(is_authenticated=True))
        assert perm.has_object_permission(request, None, obj) is True

    def test_write_method_owner_allowed(self):
        perm = IsOwnerOrReadOnly()
        user = MagicMock(is_authenticated=True)
        obj = MagicMock()
        obj.visibility = "private"
        obj.owner = user
        request = self._make_request("PUT", user)
        assert perm.has_object_permission(request, None, obj) is True

    def test_write_method_non_owner_denied(self):
        perm = IsOwnerOrReadOnly()
        owner = MagicMock(is_authenticated=True)
        other = MagicMock(is_authenticated=True)
        obj = MagicMock()
        obj.owner = owner
        request = self._make_request("DELETE", other)
        assert perm.has_object_permission(request, None, obj) is False
