from _winapi import NULL
from django.db import models, transaction

from sucursal.models import Empleado
from products.models import Product
from decimal import Decimal
from datetime import time

class Cliente(models.Model):
    nombre = models.CharField(max_length=20, blank=True)
    dni = models.IntegerField(blank=True)

    def __str__(self):
        return f"""NOMBRE: {self.nombre.upper()} - DNI: {self.dni}"""


class Caja(models.Model):
    numeroCaja = models.IntegerField(unique=True, null=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.DO_NOTHING)
    fecha = models.DateField(auto_now_add=True, null=True, blank=True)
    apertura = models.TimeField(blank=True, null=True)
    cierre = models.TimeField(blank=True, null=True) 
    class Estado(models.TextChoices):
        ACTIVA = 'ACT', 'Activa'
        CERRADA = 'CER', 'Cerrada'
    estado = models.CharField(max_length=3, choices=Estado.choices)
    historial_cierres = models.JSONField(default=list)
    def get_empleado(self):
        return self.empleado 
    def get_numeroCaja(self):
        return self.numeroCaja
    def save(self, *args, **kwargs):
        if not self.numeroCaja:
            ultimo_numeroCaja = Caja.objects.all().order_by('-numeroCaja').first()
            self.numeroCaja = (ultimo_numeroCaja.numeroCaja + 1) if ultimo_numeroCaja else 1
        super().save(*args, **kwargs)
    def __str__(self):
        return f'NUMERO CAJA: {self.numeroCaja} - EMPLEADO: {self.empleado}' 


class Venta(models.Model):
    numero_venta = models.IntegerField(unique=True, blank=True)
    caja = models.ForeignKey(Caja, on_delete=models.PROTECT) 
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    class metodoPago(models.TextChoices):
        EFECTIVO = 'EFE', 'Efectivo'
        CREDITO = 'CRE', 'Credito'
        DEBITO = 'DEB', 'Debito'
        TRASNFERENCIA = 'TRA', 'Transferencia'
    metodo_pago = models.CharField(max_length=3, choices=metodoPago.choices, default=metodoPago.EFECTIVO)
    class estadoVenta(models.TextChoices):
        FINALIZADA = "FIN", 'Finalizada',
        EN_PROCESO = "PRC", 'En proceso',
        PENDIENTE = 'PEN', 'Pendiente'
    estado_venta = models.CharField(max_length=3, choices=estadoVenta.choices, default=estadoVenta.PENDIENTE)
    def save(self, *args, **kwargs):
        if not self.numero_venta:
            ultima_venta = Venta.objects.all().order_by('-numero_venta').first()
            self.numero_venta = (ultima_venta.numero_venta + 1) if ultima_venta else 1
        super().save(*args, **kwargs)
        
    def convertir_fecha(self, anio, mes):
        return self.objects.filter(fecha__year=anio, fecha__month=mes)


    def get_info_venta(self):
        return f'VENTA N°: {self.numero_venta} - FECHA: {self.fecha} - HORA: {self.hora} - CLIENTE: {self.cliente} - METODO PAGO: {self.metodo_pago}'

    @property
    def set_cliente(self):
        return self.cliente   

    def calcular_total(self):
        total = sum(detalle.subtotal() for detalle in self.detalles.all())
        return total

    def mostrar_detalle(self):
        return (detalle.get_detalle() for detalle in self.detalles.all())
    
    def mostrar_hora(self):
        return f'{self.fecha} {self.hora}'
    
    def mostrar_pago(self):
        return (self.metodo_pago)
    
    def __str__(self):
        return f"{self.numero_venta}"
    


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    descuento = models.IntegerField(default=0, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.precio_unitario:
            self.precio_unitario = self.producto.price
        super().save(*args, **kwargs)

    def subtotal(self):
        subtotal = self.precio_unitario * self.cantidad
        descuento = self.descuento
        if descuento:
            descuento = subtotal * (Decimal(descuento) / Decimal(100))
            subtotal = subtotal - descuento
        return subtotal
    
    def get_detalle(self):
        return f""" PRODUCTO: {self.producto} - CANTIDAD: {self.cantidad} - SUBTOTAL: {self.subtotal()}'"""