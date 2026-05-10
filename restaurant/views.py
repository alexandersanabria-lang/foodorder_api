# ViewSets para Plato y Pedido
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Plato, Pedido
from .serializers import PlatoSerializer, PedidoSerializer


class PlatoViewSet(viewsets.ModelViewSet):
    queryset = Plato.objects.all()
    serializer_class = PlatoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categoria', 'disponible']
    search_fields = ['nombre', 'categoria', 'descripcion']
    ordering_fields = ['nombre', 'precio', 'categoria']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        nombre = instance.nombre
        self.perform_destroy(instance)
        return Response(
            {"mensaje": f"Plato '{nombre}' eliminado correctamente."},
            status=status.HTTP_200_OK
        )


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.prefetch_related('detallepedido_set__plato').all()
    serializer_class = PedidoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado']
    search_fields = ['cliente', 'estado']
    ordering_fields = ['fecha', 'total', 'estado']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        pid = instance.id
        self.perform_destroy(instance)
        return Response(
            {"mensaje": f"Pedido #{pid} eliminado correctamente."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], url_path='cambiar-estado')
    def cambiar_estado(self, request, pk=None):
        pedido = self.get_object()
        nuevo_estado = request.data.get('estado')
        estados_validos = [s[0] for s in Pedido.ESTADO_CHOICES]
        if nuevo_estado not in estados_validos:
            return Response(
                {"error": f"Estado inválido. Opciones: {estados_validos}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        pedido.estado = nuevo_estado
        pedido.save()
        serializer = self.get_serializer(pedido)
        return Response(serializer.data)