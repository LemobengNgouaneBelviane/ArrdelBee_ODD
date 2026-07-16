from rest_framework import serializers
from .models import Region, Department, Commune

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name", "code"]


class DepartmentSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Department
        fields = ["id", "name", "code", "region"]


class CommuneSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Commune
        fields = ["id", "name", "code", "department"]
