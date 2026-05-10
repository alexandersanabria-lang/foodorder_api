from django.db import models


class Plato(models.Model):
    CATEGORIA_CHOICES = [
        ('entrada', 'Entrada'),
        ('plato_principal', 'Plato Principal'),
        ('postre', 'Postre'),
        ('bebida', 'Bebida'),
    ]

    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    descripcion = models.TextField(blank=True, default='')
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} (S/ {self.precio})"

    class Meta:
        ordering = ['categoria', 'nombre']


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_preparacion', 'En Preparación'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    cliente = models.CharField(max_length=200, default='Cliente')
    platos = models.ManyToManyField(Plato, through='DetallePedido', related_name='pedidos')

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente} ({self.estado})"

    def calcular_total(self):
        total = sum(
            detalle.plato.precio * detalle.cantidad
            for detalle in self.detallepedido_set.all()
        )
        self.total = total
        self.save(update_fields=['total'])
        return total

    class Meta:
        ordering = ['-fecha']


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad}x {self.plato.nombre}"

    class Meta:
        unique_together = ['pedido', 'plato']