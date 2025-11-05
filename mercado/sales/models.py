from django.db import models
from sucursal.models import Empleado


class Cliente(models.Model):
    nombre = models.CharField(max_length=20, blank=True)
    dni = models.IntegerField(blank=True)
    class metodoPago(models.TextChoices):
        EFECTIVO = 'EFE', 'Efectivo'
        CREDITO = 'CRE', 'Credito'
        DEBITO = 'DEB', 'Debito'
        TRASNFERENCIA = 'TRA', 'Transferencia'
    metodo_pago = models.CharField(max_length=3, choices=metodoPago.choices)

    def __str__(self):
        return f"""
        NOMBRE{self.nombre}
        DNI:{self.dni} 
        PAGO:{self.metodo_pago}"""


class Caja(models.Model):
    numeroCaja = models.IntegerField()
    empleado = models.OneToOneField(Empleado, on_delete=models.DO_NOTHING)
    class Estado(models.TextChoices):
        ACTIVA = 'ACT', 'Activa'
        CERRADA = 'CER', 'Cerrada'
    estado = models.CharField(max_length=3, choices=Estado.choices)

    def get_empleado(self):
        return self.empleado
    def get_numeroCaja(self):
        return self.numeroCaja

class Venta(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2)
    caja = models.OneToOneField(Caja, on_delete=models.DO_NOTHING)
    cliente = models.OneToOneField(Cliente, on_delete=models.DO_NOTHING)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"""
TOTAL: {self.total}
NUMERO CAJA: {self.caja.get_numeroCaja}
EMPLEADO: {self.caja.get_empleado}
CLIENTE: {self.cliente}
"""

