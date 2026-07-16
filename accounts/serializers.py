from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone

from locations.models import Region, Department, Commune
from locations.serializers import RegionSerializer, DepartmentSerializer, CommuneSerializer

from .models import User, Role
from .models import User, PasswordResetCode

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "description", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    commune = CommuneSerializer(read_only=True)
    roles = RoleSerializer(many=True, read_only=True)
    profile_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "email", "full_name", "phone",
            "level", "region", "department", "commune",
            "roles", "profile_photo_url",
            "is_active", "date_joined", "updated_at",
        ]
        read_only_fields = ["is_active", "date_joined", "updated_at"]

    def get_profile_photo_url(self, obj: User):
        request = self.context.get("request")
        if obj.profile_photo and hasattr(obj.profile_photo, "url"):
            if request:
                return request.build_absolute_uri(obj.profile_photo.url)
            return obj.profile_photo.url
        return None


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    region_id = serializers.IntegerField(required=False, allow_null=True)
    department_id = serializers.IntegerField(required=False, allow_null=True)
    commune_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "email", "password", "full_name", "phone",
            "level", "region_id", "department_id", "commune_id",
            "profile_photo",
        ]

    def validate_password(self, value: str):
        password_validation.validate_password(value)
        return value

    def validate(self, attrs):
        level = attrs.get("level", User.Level.NATIONAL)
        region_id = attrs.get("region_id")
        department_id = attrs.get("department_id")
        commune_id = attrs.get("commune_id")

        region = department = commune = None

        # Règles de cohérence selon niveau
        if level == User.Level.NATIONAL:
            if any([region_id, department_id, commune_id]):
                raise serializers.ValidationError("Niveau NATIONAL: ne pas fournir région/département/commune.")

        elif level == User.Level.REGIONAL:
            if not region_id:
                raise serializers.ValidationError("Niveau REGIONAL: region_id requis.")
            region = Region.objects.filter(id=region_id).first()
            if not region:
                raise serializers.ValidationError("region_id invalide.")
            if department_id or commune_id:
                raise serializers.ValidationError("Niveau REGIONAL: ne pas fournir department_id/commune_id.")

        elif level == User.Level.DEPARTEMENTAL:
            if not department_id:
                raise serializers.ValidationError("Niveau DEPARTEMENTAL: department_id requis.")
            department = Department.objects.select_related("region").filter(id=department_id).first()
            if not department:
                raise serializers.ValidationError("department_id invalide.")
            region = department.region
            if commune_id:
                raise serializers.ValidationError("Niveau DEPARTEMENTAL: ne pas fournir commune_id.")
            if region_id and region_id != region.id:
                raise serializers.ValidationError("region_id ne correspond pas au département fourni.")

        elif level == User.Level.COMMUNAL:
            if not commune_id:
                raise serializers.ValidationError("Niveau COMMUNAL: commune_id requis.")
            commune = Commune.objects.select_related("department", "department__region").filter(id=commune_id).first()
            if not commune:
                raise serializers.ValidationError("commune_id invalide.")
            department = commune.department
            region = department.region
            if department_id and department_id != department.id:
                raise serializers.ValidationError("department_id ne correspond pas à la commune fournie.")
            if region_id and region_id != region.id:
                raise serializers.ValidationError("region_id ne correspond pas à la commune fournie.")
        else:
            raise serializers.ValidationError("Niveau invalide.")

        # stocker objets résolus pour create()
        attrs["_resolved_region"] = region
        attrs["_resolved_department"] = department
        attrs["_resolved_commune"] = commune
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("region_id", None)
        validated_data.pop("department_id", None)
        validated_data.pop("commune_id", None)

        region = validated_data.pop("_resolved_region", None)
        department = validated_data.pop("_resolved_department", None)
        commune = validated_data.pop("_resolved_commune", None)

        user = User.objects.create_user(**validated_data, password=password)
        user.region = region
        user.department = department
        user.commune = commune
        user.save(update_fields=["region", "department", "commune"])
        return user


class MeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["full_name", "phone", "profile_photo"]


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

    def validate(self, attrs):
        user: User = self.context["request"].user
        if not user.check_password(attrs["current_password"]):
            raise serializers.ValidationError("Mot de passe actuel incorrect.")
        return attrs

    def save(self, **kwargs):
        user: User = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user


class ArrdelTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Ajoute quelques infos utiles dans la réponse login.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["level"] = user.level
        token["roles"] = list(user.roles.values_list("name", flat=True))
        return token
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=4, max_length=10)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

    def validate(self, attrs):
        email = attrs["email"].strip().lower()
        code = attrs["code"].strip()

        user = User.objects.filter(email__iexact=email).first()
        if not user or not user.is_active:
            # ⚠️ On ne révèle rien : on laisse passer et on échouera plus tard proprement
            attrs["_user"] = None
            return attrs

        reset = (
            PasswordResetCode.objects
            .filter(user=user, used_at__isnull=True, expires_at__gt=timezone.now())
            .order_by("-created_at")
            .first()
        )

        if not reset or not reset.verify_code(code):
            raise serializers.ValidationError("Code invalide ou expiré.")

        attrs["_user"] = user
        attrs["_reset_obj"] = reset
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["_user"]
        reset_obj = self.validated_data["_reset_obj"]
        new_password = self.validated_data["new_password"]

        user.set_password(new_password)
        user.save(update_fields=["password"])

        reset_obj.mark_used()
        return user