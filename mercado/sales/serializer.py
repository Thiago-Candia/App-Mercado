from rest_framework import serializers
from .models import Venta, Caja, Cliente
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
    class Meta:
        model = Venta
        fields = '__all__'


# SerializerMethodField() sirve para incluir un campo calculado (subtotal).

class DetalleVenta(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()
    class Meta:
        model = Venta
        fields = '__all__'

    def get_subtotal(self, obj):
        return obj.producto.price * obj.cantidad
    