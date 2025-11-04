from django.db import models
from django.db.models import Sum, F
from django.contrib.auth.models import User  # Para enlazar con el Cliente/Usuario
from products.models import Product          # Para enlazar con los productos
from django.conf import settings             # Forma correcta de referirse al User

# --- Modelos de la App 'sales' ---

class Caja(models.Model):
    """
    Representa una caja registradora en una sede.
    """
    numero = models.PositiveIntegerField(unique=True)
    # podrías añadir una FK a 'Sede' si tienes varias sedes
    # sede = models.ForeignKey(Sede, on_delete=models.PROTECT)
    
    def __str__(self):
        return f'Caja N° {self.numero}'


class Pago(models.Model):
    """
    El "recibo" o la transacción general.
    Contiene el total y la información del cliente.
    """
    
    # --- Opciones para campos 'choices' ---
    class MetodoPago(models.TextChoices):
        EFECTIVO = 'EFE', 'Efectivo'
        TARJETA = 'TAR', 'Tarjeta'
        TRANSFERENCIA = 'TRA', 'Transferencia'
        
    class EstadoPago(models.TextChoices):
        PENDIENTE = 'PEN', 'Pendiente'
        COMPLETADO = 'COM', 'Completado'
        CANCELADO = 'CAN', 'Cancelado'

    # --- Claves Foráneas (FK) ---
    # Quién pagó. Usamos el modelo User de Django que configuramos en settings.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='pagos')
    # Dónde se procesó el pago
    caja = models.ForeignKey(Caja, on_delete=models.PROTECT, related_name='pagos')
    
    # --- Atributos del Pago ---
    # Este total se calculará automáticamente
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    metodo_pago = models.CharField(
        max_length=3,
        choices=MetodoPago.choices,
        default=MetodoPago.EFECTIVO
    )
    estado = models.CharField(
        max_length=3,
        choices=EstadoPago.choices,
        default=EstadoPago.PENDIENTE
    )
    
    # Timestamps (los tenías bien)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Clave Primaria (PK)
    # Django añade un 'id' automáticamente, que es la PK.
    # A veces se añade un ID público (UUID) para los recibos.
    # id_transaccion = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        # Muestra el ID (PK), el username del user y el total.
        return f'Pago #{self.id} - {self.user.username} - ${self.total}'


class PagoDetalle(models.Model):
    """
    Cada ítem individual dentro de un Pago.
    (Ej: 3 x Gaseosa, 1 x Pan)
    """
    
    # --- Claves Foráneas (FK) ---
    # A qué recibo pertenece esta línea
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE, related_name='detalles')
    # Qué producto se vendió
    producto = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='ventas')
    
    # --- Atributos del Detalle ---
    # La cantidad de este producto (¡aquí va la cantidad!)
    cantidad = models.PositiveIntegerField(default=1)
    
    # ¡MUY IMPORTANTE!
    # Guardamos el precio del producto AL MOMENTO de la venta.
    # Si el precio del producto cambia mañana, el recibo de hoy no debe cambiar.
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Este subtotal se calculará automáticamente
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.name} @ ${self.precio_unitario}'
    
    def save(self, *args, **kwargs):
        # 1. Antes de guardar, "congela" el precio del producto
        self.precio_unitario = self.producto.price
        # 2. Calcula el subtotal de esta línea
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)