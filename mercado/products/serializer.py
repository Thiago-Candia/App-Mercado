
from rest_framework import serializers
from .models import Product, Catalogo, CategoriaProducto, SubCategoriaProducto

class CatalogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProducto
        fields = '__all__'

class SubCategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoriaProducto
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'