from django.db import models, transaction
from sucursal.models import Empleado
from products.models import Product


class Cliente(models.Model):
    nombre = models.CharField(max_length=20, blank=True)
    dni = models.IntegerField(blank=True)
    pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)  

    
    def __str__(self):
        return f"""NOMBRE: {self.nombre.upper()} - DNI: {self.dni}"""


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
    numero_venta = models.IntegerField(unique=True, blank=False)
    caja = models.ForeignKey(Caja, on_delete=models.PROTECT) 
    fecha = models.DateTimeField(auto_now=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    class metodoPago(models.TextChoices):
        EFECTIVO = 'EFE', 'Efectivo'
        CREDITO = 'CRE', 'Credito'
        DEBITO = 'DEB', 'Debito'
        TRASNFERENCIA = 'TRA', 'Transferencia'
    metodo_pago = models.CharField(max_length=3, choices=metodoPago.choices, default=metodoPago.EFECTIVO)

    def save(self, *args, **kwargs):
        if not self.numero_venta:
            ultima_venta = Venta.objects.all().order_by('-numero_venta').first()
            self.numero_venta = (ultima_venta.numero_venta + 1) if ultima_venta else 1
            super().save(*args, **kwargs)
        
    @property
    def set_cliente(self):
        return self.cliente    
    def calcular_total(self):
        return sum(detalle.subtotal() for detalle in self.detalles.all())
    
    def mostrar_detalle(self):
        return (detalle.get_detalle() for detalle in self.detalles.all())
    
    def mostrar_hora(self):
        return f'{self.fecha.strftime('%d/%m/%Y %H:%M')}'
    
    def mostrar_pago(self):
        return (self.metodo_pago)
    
    def ingresar_pago(self):
        return self.cliente.pago
    
    def __str__(self):
        return f"{self.numero_venta}"
    


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.precio_unitario:
            self.precio_unitario = self.producto.price
        super().save(*args, **kwargs)

    def subtotal(self):
        return self.precio_unitario * self.cantidad
    
    def get_detalle(self):
        return f""" PRODUCTO: {self.producto} - CANTIDAD: {self.cantidad} {self.subtotal()}'"""