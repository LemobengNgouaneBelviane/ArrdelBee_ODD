from django.urls import path
from .views import RegionListAPIView, DepartmentListAPIView, CommuneListAPIView

urlpatterns = [
    path("locations/regions/", RegionListAPIView.as_view(), name="regions-list"),
    path("locations/departments/", DepartmentListAPIView.as_view(), name="departments-list"),
    path("locations/communes/", CommuneListAPIView.as_view(), name="communes-list"),
]
