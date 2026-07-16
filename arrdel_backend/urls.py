from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Arrdel API",
      default_version='v1',
      description="Documentation Officielle des API Arrdel (incl. Module ODD)",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Swagger Documentation API
    path("docs/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path("api/", include("accounts.urls")),
    path("api/", include("locations.urls")),
    path("api/odd/", include("odd.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
