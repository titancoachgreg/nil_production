from rest_framework.routers import DefaultRouter
from djangoapp.api.views import SchoolViewSet, SportAliasViewSet, SportViewSet, EndpointTypeViewSet

router = DefaultRouter()
router.register(r'ncaa-directory', SchoolViewSet, basename='ncaa-directory')
router.register(r'sports', SportViewSet, basename='sports')
router.register(r'endpoint-types', EndpointTypeViewSet, basename='endpoint-types')
router.register(r'sport-aliases', SportAliasViewSet, basename='sport-aliases')

urlpatterns = router.urls
