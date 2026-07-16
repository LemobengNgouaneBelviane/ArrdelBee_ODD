from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password

import secrets

from .managers import UserManager


def profile_photo_path(instance, filename: str) -> str:
    return f"profiles/user_{instance.id}/{filename}"


class Role(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PasswordResetCode(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_codes",
    )
    code_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    last_sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "expires_at"]),
            models.Index(fields=["user", "used_at"]),
        ]

    def verify_code(self, raw_code: str) -> bool:
        return check_password(raw_code, self.code_hash)

    def mark_used(self):
        self.used_at = timezone.now()
        self.save(update_fields=["used_at"])

    @staticmethod
    def generate_code() -> str:
        return f"{secrets.randbelow(9000) + 1000}"  # 4 chiffres

    @classmethod
    def create_for_user(cls, user, ttl_minutes: int = 10):
        raw = cls.generate_code()
        obj = cls.objects.create(
            user=user,
            code_hash=make_password(raw),
            expires_at=timezone.now() + timezone.timedelta(minutes=ttl_minutes),
        )
        return obj, raw

    def __str__(self):
        return f"ResetCode(user={self.user_id}, created_at={self.created_at}, used={self.used_at is not None})"
class User(AbstractBaseUser, PermissionsMixin):
    class Level(models.TextChoices):
        COMMUNAL = "COMMUNAL", "Communal"
        DEPARTEMENTAL = "DEPARTEMENTAL", "Départemental"
        REGIONAL = "REGIONAL", "Régional"
        NATIONAL = "NATIONAL", "National"

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40, blank=True, default="")

    level = models.CharField(max_length=20, choices=Level.choices, default=Level.NATIONAL)

    # Localisation (selon niveau)
    region = models.ForeignKey(
        "locations.Region", null=True, blank=True, on_delete=models.SET_NULL, related_name="users"
    )
    department = models.ForeignKey(
        "locations.Department", null=True, blank=True, on_delete=models.SET_NULL, related_name="users"
    )
    commune = models.ForeignKey(
        "locations.Commune", null=True, blank=True, on_delete=models.SET_NULL, related_name="users"
    )

    profile_photo = models.ImageField(upload_to=profile_photo_path, null=True, blank=True)

    roles = models.ManyToManyField(Role, through="UserRole", blank=True, related_name="users")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_active", "deleted_at"])

    def __str__(self):
        return self.email


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "role")

    def __str__(self):
        return f"{self.user.email} -> {self.role.name}"


