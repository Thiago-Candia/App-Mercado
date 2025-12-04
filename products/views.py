from django.shortcuts import render
from rest_framework import viewsets, status
from .serializer import ProductSerializer
from .models import Product
from .serializer import ProductSerializer, CatalogoSerializer, CategoriaSerializer, ProductoStockNuevoSerializer ,SubCategoriaSerializer, ProductoPrecioNuevoSerializer, CodigoSerializer
from .models import Product, Catalogo, CategoriaProducto, SubCategoriaProducto
from rest_framework.decorators import action
from django.db import transaction



""" PARA BUSCAR PRODUCTOS POR NOMBRE """
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import filters
from django.db.models import Q

# Create your views here.

class CatalogoViewSet(viewsets.ModelViewSet):
    serializer_class = CatalogoSerializer
    queryset = Catalogo.objects.all()

class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    queryset = CategoriaProducto.objects.all()

class SubCategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategoriaSerializer
    queryset = SubCategoriaProducto.objects.all()

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    @transaction.atomic
    @action(detail=True, methods=['get','post'], serializer_class=ProductoPrecioNuevoSerializer)
    def cambiar_precio(self, request, pk=Product.pk):
        serializer = ProductoPrecioNuevoSerializer(data=request.data)
        producto = self.get_object()
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        nuevo_precio = serializer.validated_data['nuevo_precio']
        producto.price = nuevo_precio
        producto.save()
        return Response({'precio': nuevo_precio})

    @transaction.atomic
    @action(detail=True, methods=['get','post'], serializer_class=ProductoStockNuevoSerializer)
    def cambiar_stock(self, request, pk=Product.pk):
        serializer = ProductoStockNuevoSerializer(data=request.data)
        producto = self.get_object()
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        nuevo_stock = serializer.validated_data['nuevo_stock']
        producto.stock = nuevo_stock
        producto.save()
        return Response({'stock': nuevo_stock})



""" 
FUNCION GLOBAL PARA BUSCAR PRODUCTOS POR NOMBRE
Q -> query set models de django
Si lo que se ingresa en la query es igual al nombre/codigo devuelve el producto
"""

@api_view(['GET'])
def buscar_productos(request):
    query = request.GET.get('search', '').strip()

    if query == '':
        return Response([])
    
    productos = Product.objects.filter(
        Q(name__icontains=query) | Q(codigo__icontains=query)
    )
    # se pasa el contexto del request para construir URLs absoluta
    serializer = ProductSerializer(productos, many=True, context={'request': request})
    return Response(serializer.data)

