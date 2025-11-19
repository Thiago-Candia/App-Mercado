from django.shortcuts import render
from rest_framework import viewsets
from .serializer import ProductSerializer
from .models import Product
from .serializer import ProductSerializer, CatalogoSerializer, CategoriaSerializer, SubCategoriaSerializer
from .models import Product, Catalogo, CategoriaProducto, SubCategoriaProducto

""" PARA BUSCAR PRODUCTOS POR NOMBRE """
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import filters



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
    """ Filter Buscador por nombre """
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']



""" FUNCION GLOBAL PARA BUSCAR PRODUCTOS POR NOMBRE """
@api_view(['GET'])
def buscar_productos(request):
    query = request.GET.get('search', '')
    productos = Product.objects.filter(name__icontains=query)
    serializer = ProductSerializer(productos, many=True)
    return Response(serializer.data)
