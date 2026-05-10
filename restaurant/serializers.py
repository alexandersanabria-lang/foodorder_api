# Serializers para Plato y Pedido
from rest_framework import serializers
from .models import Plato, Pedido, DetallePedido


class PlatoSerializer(serializers.ModelSerializer):
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)

    class Meta:
        model = Plato
        fields = ['id', 'nombre', 'precio', 'categoria', 'categoria_display', 'descripcion', 'disponible']


class DetallePedidoSerializer(serializers.ModelSerializer):
    plato_nombre = serializers.CharField(source='plato.nombre', read_only=True)
    plato_precio = serializers.DecimalField(source='plato.precio', max_digits=8, decimal_places=2, read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = DetallePedido
        fields = ['plato', 'plato_nombre', 'plato_precio', 'cantidad', 'subtotal']

    def get_subtotal(self, obj):
        return obj.plato.precio * obj.cantidad


class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(source='detallepedido_set', many=True, read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    platos_resumen = serializers.SerializerMethodField()

    items = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Pedido
        fields = [
            'id', 'cliente', 'fecha', 'estado', 'estado_display',
            'total', 'detalles', 'platos_resumen', 'items'
        ]
        read_only_fields = ['fecha', 'total']

    def get_platos_resumen(self, obj):
        return [
            f"{d.cantidad}x {d.plato.nombre}"
            for d in obj.detallepedido_set.select_related('plato').all()
        ]

    def _save_items(self, pedido, items):
        pedido.detallepedido_set.all().delete()
        for item in items:
            plato_id = item.get('plato')
            cantidad = item.get('cantidad', 1)
            try:
                plato = Plato.objects.get(id=plato_id)
                DetallePedido.objects.create(pedido=pedido, plato=plato, cantidad=cantidad)
            except Plato.DoesNotExist:
                raise serializers.ValidationError(f"Plato con id {plato_id} no existe.")
        pedido.calcular_total()

    def create(self, validated_data):
        items = validated_data.pop('items', [])
        pedido = Pedido.objects.create(**validated_data)
        if items:
            self._save_items(pedido, items)
        return pedido

    def update(self, instance, validated_data):
        items = validated_data.pop('items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if items is not None:
            self._save_items(instance, items)
        return instance