from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterAPIView, LoginAPIView, RefreshAPIView,
    MeAPIView, ChangePasswordAPIView, DeactivateMeAPIView,
    RoleViewSet, UserAdminViewSet,
    ForgotPasswordAPIView, ResetPasswordAPIView,
)

router = DefaultRouter()
router.register(r"admin/roles", RoleViewSet, basename="admin-roles")
router.register(r"admin/users", UserAdminViewSet, basename="admin-users")

urlpatterns = [
    # Auth
    path("auth/register/", RegisterAPIView.as_view(), name="auth-register"),
    path("auth/login/", LoginAPIView.as_view(), name="auth-login"),
    path("auth/refresh/", RefreshAPIView.as_view(), name="auth-refresh"),
    
     path("auth/password/forgot/", ForgotPasswordAPIView.as_view(), name="auth-forgot-password"),
    path("auth/password/reset/", ResetPasswordAPIView.as_view(), name="auth-reset-password"),


    # Profil utilisateur
    path("users/me/", MeAPIView.as_view(), name="me"),
    path("users/me/change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("users/me/deactivate/", DeactivateMeAPIView.as_view(), name="deactivate-me"),

    # Admin routes
    path("", include(router.urls)),
]
