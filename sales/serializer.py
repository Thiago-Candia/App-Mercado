from rest_framework import serializers
from .models import Venta, Caja, Cliente, DetalleVenta, Product
from sucursal.models import Empleado
from rest_framework.decorators import action
from django.db import transaction

class CajaSerializer(serializers.ModelSerializer):
    empleado = serializers.StringRelatedField(read_only=True)
    empleado_id = serializers.PrimaryKeyRelatedField(
    queryset=Empleado.objects.all(),
    source='empleado',
    write_only=True
    )
    class Meta:
        model = Caja
        fields = ['numeroCaja', 'empleado', 'empleado_id']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nombre','dni']

class CobrarSerializer(serializers.Serializer):
    venta_id = serializers.PrimaryKeyRelatedField(
    queryset=Venta.objects.all(),
    source='venta',
    write_only=True
    )
    monto_recibido=serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True
    )

class VentaSerializer(serializers.ModelSerializer):
    caja = serializers.StringRelatedField(read_only=True)
    caja_id = serializers.PrimaryKeyRelatedField(
    queryset=Caja.objects.all(),
    source='caja',
    write_only=True
    )
    cliente = serializers.StringRelatedField(read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset= Cliente.objects.all(),
        source='cliente',
        write_only=True
    )

    total = serializers.SerializerMethodField()
    def get_total(self, obj):
        return obj.calcular_total()
    
    detalles = serializers.SerializerMethodField()
    def get_detalles(self, obj):
        return obj.mostrar_detalle()
        try:
            return obj.calcular_total() if obj.pk else []
        except Exception:
            return 0
    
    detalles = serializers.SerializerMethodField()
    def get_detalles(self, obj):
        return obj.mostrar_detalle() if obj.pk else []
    
    fecha = serializers.SerializerMethodField()
    def get_fecha(self, obj):
        return obj.mostrar_hora()
    
    metodo_pago = serializers.SerializerMethodField()
    def get_metodo_pago(self, obj):
        return obj.mostrar_pago()
    

    class Meta:
        model = Venta
        fields = '__all__'


class DetalleVentaSerializer(serializers.ModelSerializer):
    venta = serializers.StringRelatedField(read_only=True)
    venta_id = serializers.PrimaryKeyRelatedField(
    queryset=Venta.objects.all(),
    source='venta',
    write_only=True
    )
    producto = serializers.StringRelatedField(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(
    queryset=Product.objects.all(),
    source='producto',
    write_only=True
    )
    class Meta:
        model = DetalleVenta
        fields = ['venta_id','venta', 'producto','producto_id', 'cantidad']


class VentasPorDiaSerializer(serializers.ModelSerializer):
    fecha_filtrada = serializers.DateField(write_only=True)
    class Meta:
        model = Venta
        fields = ['fecha','fecha_filtrada']
    detalles = serializers.SerializerMethodField(read_only=True)
    def get_detalles(self, obj):
        return obj.mostrar_detalle() if obj.pk else []  
    info = serializers.SerializerMethodField(read_only=True)
    def get_info(self, obj):
        return obj.get_info_venta()
    
    class Meta:
        model = Venta
        fields = ['fecha_filtrada', 'detalles', 'info']
