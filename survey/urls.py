from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from survey.views import *
from survey.yasg import generate_api_description, SurveySchemaGenerator

router = routers.DefaultRouter()
router.register(r'surveys', SurveyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Survey API",
        default_version="v1",
        description=generate_api_description()
    ),
    public=False,
    permission_classes=(permissions.IsAuthenticated,),
    generator_class=SurveySchemaGenerator,
    patterns=urlpatterns,
)

urlpatterns += [
    path(
        "swagger/<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="swagger-yaml",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]