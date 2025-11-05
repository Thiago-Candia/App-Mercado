from django.shortcuts import render
from rest_framework import viewsets
from .serializer import ProductSerializer, CatalogoSerializer, CategoriaSerializer, SubCategoriaSerializer
from .models import Product, Catalogo, CategoriaProducto, SubCategoriaProducto

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
