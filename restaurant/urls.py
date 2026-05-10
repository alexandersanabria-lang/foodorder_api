# URLs para la app restaurant
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlatoViewSet, PedidoViewSet

router = DefaultRouter()
router.register(r'platos', PlatoViewSet, basename='plato')
router.register(r'pedidos', PedidoViewSet, basename='pedido')

urlpatterns = [
    path('', include(router.urls)),
]