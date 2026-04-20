from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)


class DemoLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Demo user for evaluator access without registration friction.
        demo_username = "demo_user"
        demo_password = "Demo@12345"
        demo_email = "demo.user@example.com"

        user, created = User.objects.get_or_create(
            username=demo_username,
            defaults={"email": demo_email},
        )
        if created or not user.check_password(demo_password):
            user.set_password(demo_password)
            user.save(update_fields=["password"])

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "Demo login successful.",
                "username": demo_username,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )