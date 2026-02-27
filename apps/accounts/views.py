from django.contrib.auth import get_user_model
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, RegisterSerializer

User = get_user_model()



class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)
        data = {
            "user": UserSerializer(user).data,
            "profile": UserProfileSerializer(profile).data,
        }
        return Response(data)

    def patch(self, request):
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)
        serializer = UserProfileSerializer(
            profile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    """
    GET  /api/auth/register/ → affiche le formulaire (browsable API)
    POST /api/auth/register/ → inscription
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        # Permet d'afficher le formulaire dans le browsable API
        serializer = self.get_serializer()
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        profile, _ = UserProfile.objects.get_or_create(user=user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "profile": UserProfileSerializer(profile).data,
            },
            status=status.HTTP_201_CREATED,
        )

