from django.utils import timezone
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import User, PasswordResetCode
from .services import send_code_via_email_service

from .models import User, Role
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    MeUpdateSerializer,
    ChangePasswordSerializer,
    RoleSerializer,
    ArrdelTokenObtainPairSerializer,
)
from .permissions import IsAdmin

from .models import User, PasswordResetCode
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer

# Optionnel: si tu utilises ton microservice email
import requests

class ForgotPasswordAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data["email"].strip().lower()

        # Réponse neutre (anti-enumération)
        neutral = Response(
            {"detail": "Si ce compte existe, un code de réinitialisation a été envoyé."},
            status=status.HTTP_200_OK,
        )

        user = User.objects.filter(email__iexact=email).first()
        if not user or not user.is_active:
            return neutral

        # Anti-spam simple : renvoi max toutes les 60 sec
        last = PasswordResetCode.objects.filter(user=user).order_by("-created_at").first()
        if last and last.last_sent_at and (timezone.now() - last.last_sent_at).total_seconds() < 60:
            return neutral

        reset_obj, raw_code = PasswordResetCode.create_for_user(user=user, ttl_minutes=10)

        try:
            send_code_via_email_service(email=user.email, code=raw_code, type_="reset")
            reset_obj.last_sent_at = timezone.now()
            reset_obj.save(update_fields=["last_sent_at"])
        except Exception as e:
            # Log seulement (ne pas révéler au client)
            print("EMAIL_SERVICE_ERROR:", e)

        return neutral


class ResetPasswordAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({"detail": "Mot de passe réinitialisé avec succès."}, status=status.HTTP_200_OK)

class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class LoginAPIView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ArrdelTokenObtainPairSerializer


class RefreshAPIView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


class MeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = MeUpdateSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        data = UserSerializer(request.user, context={"request": request}).data
        return Response(data)


class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Mot de passe modifié avec succès."})


class DeactivateMeAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        user: User = request.user
        user.is_active = False
        user.deleted_at = timezone.now()
        user.save(update_fields=["is_active", "deleted_at"])
        return Response({"detail": "Compte désactivé."}, status=status.HTTP_200_OK)


# ---------------- ADMIN API ----------------

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by("name")
    serializer_class = RoleSerializer
    permission_classes = [IsAdmin]


class UserAdminViewSet(viewsets.ModelViewSet):
    """
    CRUD admin des utilisateurs.
    - destroy => soft delete (désactivation)
    - action hard_delete => suppression définitive
    - actions roles: assign / remove
    """
    queryset = User.objects.select_related("region", "department", "commune").prefetch_related("roles").all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.soft_delete()
        return Response({"detail": "Utilisateur désactivé (soft delete)."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="hard-delete")
    def hard_delete(self, request, pk=None):
        user = self.get_object()
        user.delete()
        return Response({"detail": "Utilisateur supprimé définitivement."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="assign-role")
    def assign_role(self, request, pk=None):
        user = self.get_object()
        role_id = request.data.get("role_id")
        if not role_id:
            return Response({"detail": "role_id requis."}, status=status.HTTP_400_BAD_REQUEST)
        role = Role.objects.filter(id=role_id).first()
        if not role:
            return Response({"detail": "role_id invalide."}, status=status.HTTP_400_BAD_REQUEST)

        user.roles.add(role)
        return Response({"detail": f"Rôle '{role.name}' ajouté à l'utilisateur."})

    @action(detail=True, methods=["post"], url_path="remove-role")
    def remove_role(self, request, pk=None):
        user = self.get_object()
        role_id = request.data.get("role_id")
        if not role_id:
            return Response({"detail": "role_id requis."}, status=status.HTTP_400_BAD_REQUEST)
        role = Role.objects.filter(id=role_id).first()
        if not role:
            return Response({"detail": "role_id invalide."}, status=status.HTTP_400_BAD_REQUEST)

        user.roles.remove(role)
        return Response({"detail": f"Rôle '{role.name}' retiré de l'utilisateur."})
