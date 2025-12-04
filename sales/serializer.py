from typing import Required
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
        fields = ['id', 'numeroCaja', 'empleado', 'empleado_id', 'apertura', 'cierre', 'estado', 'fecha']
        extra_kwargs = {
            "fecha": {"read_only": True}
        }

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'dni']



""" 
Serializer para cobrar una venta y aplicar descuentos.
Se Elimino el campo venta_id porque la venta viene en la URL, no en el body.
"""

class CobrarSerializer(serializers.Serializer):
    monto_recibido = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True
    )
    descuento = serializers.IntegerField(
        required=False,
        default=0
    )


class DescuentoSerializer(serializers.Serializer):
    venta_id = serializers.PrimaryKeyRelatedField(
        queryset=Venta.objects.all(),
        source='venta',
        write_only=True
    )
    descuento = serializers.IntegerField(
    required=False
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
        write_only=True,
        required=False
    )
    total = serializers.SerializerMethodField()


    def get_total(self, obj):
        try:
            if obj.total > 0:
                return obj.total
            elif obj.total <= 0: 
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


    estado_venta = serializers.SerializerMethodField()
    def get_estado_venta(self, obj):
        return obj.estado_venta


    class Meta:
        model = Venta
        fields = ['id', 'caja_id', 'caja', 'cliente_id', 'cliente', 'numero_venta', 'total', 'detalles', 'fecha', 'metodo_pago', 'estado_venta'] 
        extra_kwargs= {
            "total": {"read_only": True},
            "numero_venta":{"read_only": True}
        }



class DescuentoUnitarioSerializer(serializers.Serializer):
    detalleventa_id = serializers.PrimaryKeyRelatedField(
    queryset=Venta.objects.all(),
    source='venta',
    write_only=True
    )
    descuento = serializers.IntegerField(
    required=False
    )



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
    subtotal = serializers.SerializerMethodField(read_only=True)
    def get_subtotal(self, obj):
        return obj.subtotal()
    class Meta:
        model = DetalleVenta
        fields = ['venta_id','venta', 'producto','producto_id', 'cantidad', 'descuento', 'subtotal', 'precio_unitario']
        read_only_fields = ['subtotal', 'venta']


class VentasPorDiaSerializer(serializers.ModelSerializer):
    fecha_filtrada = serializers.DateField(write_only=True)
    detalles = serializers.SerializerMethodField(read_only=True)
    def get_detalles(self, obj):
        return obj.mostrar_detalle() if obj.pk else []  
    total = serializers.SerializerMethodField(read_only=True)
    def get_total(self, obj):
        return obj.calcular_total()
    info = serializers.SerializerMethodField(read_only=True)
    def get_info(self, obj):
        return obj.get_info_venta()
    
    class Meta:
        model = Venta
        fields = ['fecha_filtrada', 'detalles', 'info', 'total']


class VentasPorMesSerializer(serializers.ModelSerializer):
    mes_filtrada = serializers.IntegerField(write_only=True)
    anio_filtrada = serializers.IntegerField(write_only=True)
    def convertir_fecha(self, obj):
        return obj.objects.filter(fecha__year=anio_filtrada, fecha__month=mes_filtrada)
    detalles = serializers.SerializerMethodField(read_only=True)
    def get_detalles(self, obj):
        return obj.mostrar_detalle() if obj.pk else []  
    info = serializers.SerializerMethodField(read_only=True)
    def get_info(self, obj):
        return obj.get_info_venta()
    total = serializers.SerializerMethodField(read_only=True)
    def get_total(self, obj):
        return obj.calcular_total()
    class Meta:
        model = Venta
        fields = ['anio_filtrada', 'mes_filtrada', 'detalles', 'info', 'total']