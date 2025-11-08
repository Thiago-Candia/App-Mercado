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
    total = models.DecimalField(max_digits=10, decimal_places=2)
    caja = models.ForeignKey(Caja, on_delete=models.PROTECT) #No borrar una caja si posee ventas
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    fecha = models.DateTimeField(auto_now_add=True)

    class metodoPago(models.TextChoices):
        EFECTIVO = 'EFE', 'Efectivo'
        CREDITO = 'CRE', 'Credito'
        DEBITO = 'DEB', 'Debito'
        TRASNFERENCIA = 'TRA', 'Transferencia'
    metodo_pago = models.CharField(max_length=3, choices=metodoPago.choices, default=metodoPago.EFECTIVO)

    def calcular_total(self):
        total = sum([DetalleVenta.subtotal for detalle in self.venta.detalles.all()])
        self.total = total
        self.save()
        return total


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

#self.price para utilizar el precio congelado del producto. En este caso si el precio cambia, no cambia el subtotal.
    def subtotal(self):
        return self.price * self.cantidad


    def __str__(self):
        return f"""
        VENTA: {self.venta} - PRODUCTO: {self.producto} - CANTIDAD: {self.cantidad}
"""