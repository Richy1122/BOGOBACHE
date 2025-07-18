from rest_framework.routers import DefaultRouter
from .views import BacheViewSet  # Asegúrate que este ViewSet existe

router = DefaultRouter()
router.register(r'baches', BacheViewSet, basename='bache')