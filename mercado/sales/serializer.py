from rest_framework import serializers
from .models import Venta, Caja, Cliente
from products.models import Product

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caja
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'