from rest_framework import generics, permissions
from .models import Region, Department, Commune
from .serializers import RegionSerializer, DepartmentSerializer, CommuneSerializer

class RegionListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Region.objects.all().order_by("name")
    serializer_class = RegionSerializer


class DepartmentListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        qs = Department.objects.select_related("region").all().order_by("name")
        region_id = self.request.query_params.get("region_id")
        if region_id:
            qs = qs.filter(region_id=region_id)
        return qs


class CommuneListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CommuneSerializer

    def get_queryset(self):
        qs = Commune.objects.select_related("department", "department__region").all().order_by("name")
        department_id = self.request.query_params.get("department_id")
        if department_id:
            qs = qs.filter(department_id=department_id)
        return qs
