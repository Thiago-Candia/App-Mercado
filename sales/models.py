from django.db import models
from sucursal.models import Empleado
from products.models import Product


class Cliente(models.Model):
    nombre = models.CharField(max_length=20, blank=True)
    dni = models.IntegerField(blank=True)

    def __str__(self):
        return f"""NOMBRE: {self.nombre} - DNI: {self.dni}"""


class Caja(models.Model):
    numeroCaja = models.IntegerField(unique=True)
    empleado = models.OneToOneField(Empleado, on_delete=models.DO_NOTHING)
    class Estado(models.TextChoices):
        ACTIVA = 'ACT', 'Activa'
        CERRADA = 'CER', 'Cerrada'
    estado = models.CharField(max_length=3, choices=Estado.choices)
    def get_empleado(self):
        return self.empleado 
    def get_numeroCaja(self):
        return self.numeroCaja
    def __str__(self):
        return f'{self.numeroCaja} {self.empleado}' 


class Venta(models.Model):
    caja = models.ForeignKey(Caja, on_delete=models.PROTECT) 
    def calcular_total(self):
        return sum(detalle.subtotal() for detalle in self.detalles.all())
    
    def mostrar_detalle(self):
        return (detalle.get_detalle() for detalle in self.detalles.all())


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.precio_unitario:
            self.precio_unitario = self.producto.price
        super().save(*args, **kwargs)

    def subtotal(self):
        return self.precio_unitario * self.cantidad

    class metodoPago(models.TextChoices):
        EFECTIVO = 'EFE', 'Efectivo'
        CREDITO = 'CRE', 'Credito'
        DEBITO = 'DEB', 'Debito'
        TRASNFERENCIA = 'TRA', 'Transferencia'
    metodo_pago = models.CharField(max_length=3, choices=metodoPago.choices, default=metodoPago.EFECTIVO)
    def get_detalle(self):
        return f""" PRODUCTO: {self.producto} - CANTIDAD: {self.cantidad} {self.subtotal()} {self.metodo_pago}  {self.fecha}'"""