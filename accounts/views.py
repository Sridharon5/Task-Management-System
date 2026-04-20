from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db import DatabaseError
from django.shortcuts import redirect

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

    @staticmethod
    def get_demo_user():
        demo_username = "demo_user"
        demo_password = "Demo@12345"
        demo_email = "demo.user@example.com"

        user, created = User.objects.get_or_create(
            username=demo_username,
            defaults={"email": demo_email},
        )
        if created or not user.check_password(demo_password):
            user.set_password(demo_password)
        user.email = demo_email
        user.is_staff = False
        user.is_superuser = False
        user.is_active = True
        user.save(update_fields=["password", "email", "is_staff", "is_superuser", "is_active"])
        return user, demo_username

    @staticmethod
    def get_demo_admin_user():
        demo_username = "demo_admin"
        demo_password = "Demo@12345"
        demo_email = "demo.admin@example.com"

        user, created = User.objects.get_or_create(
            username=demo_username,
            defaults={"email": demo_email},
        )
        if created or not user.check_password(demo_password):
            user.set_password(demo_password)
        user.email = demo_email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(update_fields=["password", "email", "is_staff", "is_superuser", "is_active"])
        return user, demo_username

    def get(self, request):
        return self.post(request)

    def post(self, request):
        try:
            user, demo_username = self.get_demo_user()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Demo user login successful.",
                    "username": demo_username,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        except DatabaseError as exc:
            return Response(
                {
                    "detail": "Database is not ready. Run migrations against your production database and retry.",
                    "error": str(exc),
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class DemoAdminPanelLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            user, _ = DemoLoginView.get_demo_admin_user()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("/admin/")
        except DatabaseError:
            return redirect("/")