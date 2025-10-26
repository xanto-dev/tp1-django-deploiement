from django.urls import path, include
from rest_framework import routers
from .views import home, statistiques, PermisAnimalViewSet, PermisConstructionViewSet, BonTravailAqueducViewSet, RegistreGESViewSet

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
        title="API des données du Quebec",
        default_version='v1',
        description="API pour gérer les données moissonnées du Quebec",
     ),
    public=True,
)

router = routers.DefaultRouter()
router.register(r'permis-animals', PermisAnimalViewSet, basename='permisanimal')
router.register(r'permis-constructions', PermisConstructionViewSet, basename='permisconstruction')
router.register(r'bon-travail-aqueduc', BonTravailAqueducViewSet, basename='bontravailaqueduc')
router.register(r'registre-ges', RegistreGESViewSet, basename='registreges')


urlpatterns = [
    path('', home, name='home'),
    path('statistiques/', statistiques, name='statistiques'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include(router.urls)),
    ]
