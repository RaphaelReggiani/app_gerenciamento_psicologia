from rest_framework.routers import DefaultRouter
from .api_views import PacientesViewSet, ConsultasViewSet, VisualizacoesViewSet, NewUserViewSet

router = DefaultRouter()
router.register(r'pacientes', PacientesViewSet)
router.register(r'consultas', ConsultasViewSet)
router.register(r'visualizacoes', VisualizacoesViewSet)
router.register(r'users', NewUserViewSet)

urlpatterns = router.urls