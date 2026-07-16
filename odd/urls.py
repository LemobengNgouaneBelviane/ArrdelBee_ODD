from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet, SectorViewSet, SDGViewSet, SND30AxisViewSet,
    OddRoleRequestViewSet, MyOddRoleView, PreuveViewSet,
    PeriodViewSet, MesureKPIViewSet,
    StatsODDView, StatsSecteurView, StatsCommuneView, CommuneProjectsView,
    CampagneReportingViewSet, RapportViewSet,
    PublicationViewSet,
    PublicProjectViewSet, ProjectExportPDFView,
    PCDObjectiveViewSet, GaddDimensionViewSet,
)

router = DefaultRouter()
router.register(r'public-projects',    PublicProjectViewSet,        basename='public-project')
router.register(r'pcd-objectives',     PCDObjectiveViewSet,         basename='pcd-objective')
router.register(r'projects',      ProjectViewSet,             basename='project')
router.register(r'sectors',       SectorViewSet,              basename='sector')
router.register(r'sdgs',          SDGViewSet)
router.register(r'snd30-axes',    SND30AxisViewSet)
router.register(r'role-requests', OddRoleRequestViewSet,      basename='odd-role-request')
router.register(r'preuves',       PreuveViewSet,              basename='preuve')
router.register(r'periods',       PeriodViewSet,              basename='period')
router.register(r'mesures',       MesureKPIViewSet,           basename='mesure')
router.register(r'campagnes',     CampagneReportingViewSet,   basename='campagne')
router.register(r'rapports',      RapportViewSet,             basename='rapport')
router.register(r'publications',  PublicationViewSet,         basename='publication')
router.register(r'gadd-dimensions', GaddDimensionViewSet, basename='gadd-dimension')

urlpatterns = [
    path('projects/<int:pk>/export-pdf/', ProjectExportPDFView.as_view(), name='project-export-pdf'),
    path('my-role/',         MyOddRoleView.as_view(),  name='odd-my-role'),
    path('stats/by-odd/',    StatsODDView.as_view(),   name='stats-by-odd'),
    path('stats/by-sector/', StatsSecteurView.as_view(), name='stats-by-sector'),
    path('stats/by-commune/', StatsCommuneView.as_view(), name='stats-by-commune'),
    path('stats/by-commune/projects/', CommuneProjectsView.as_view(), name='stats-by-commune-projects'),
    path('', include(router.urls)),
]
