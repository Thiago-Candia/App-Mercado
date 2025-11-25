import decimal
from rest_framework import serializers
from .models import Product
from .models import Product, Catalogo, CategoriaProducto, SubCategoriaProducto

class CatalogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    catalogo = serializers.StringRelatedField(read_only=True)
    catalogo_id = serializers.PrimaryKeyRelatedField(
        queryset=Catalogo.objects.all(),
        source='catalogo',
        write_only=True
    )
    class Meta:
        model = CategoriaProducto
        fields = '__all__'

class SubCategoriaSerializer(serializers.ModelSerializer):
    categoria = serializers.StringRelatedField(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=CategoriaProducto.objects.all(),
        source='categoria',
        write_only=True
    )
    class Meta:
        model = SubCategoriaProducto
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    categoria = serializers.StringRelatedField(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=CategoriaProducto.objects.all(),
        source='categoria',
        write_only=True
    )
    subcategoria = serializers.StringRelatedField()
    subcategoria_id = serializers.PrimaryKeyRelatedField(
        queryset=SubCategoriaProducto.objects.all(),
        source='subcategoria',
        write_only=True
    )
    class Meta:
        model = Product
        fields = '__all__'

class ProductoPrecioNuevoSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
    source='producto',
    write_only=True
    )
    nuevo_precio = serializers.DecimalField(max_digits=10, decimal_places=2)

class ProductoStockNuevoSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
    source='producto',
    write_only=True
    )
    nuevo_stock = serializers.IntegerField()

class CodigoSerializer(serializers.Serializer):
    codigo_filtrado = serializers.IntegerField()