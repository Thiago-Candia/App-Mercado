from rest_framework import serializers
from .models import Venta, Caja, Cliente, DetalleVenta, Product
from sucursal.models import Empleado

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
        fields = '__all__'


class VentaSerializer(serializers.ModelSerializer):
    caja = serializers.StringRelatedField(read_only=True)
    caja_id = serializers.PrimaryKeyRelatedField(
    queryset=Caja.objects.all(),
    source='caja',
    write_only=True
    )
    total = serializers.SerializerMethodField()
    def get_total(self, obj):
        return obj.calcular_total()
    detalles = serializers.SerializerMethodField()
    def get_detalles(self, obj):
        return obj.mostrar_detalle()
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
        fields = '__all__'