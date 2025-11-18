from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializer import CajaSerializer, VentaSerializer, ClienteSerializer
from .models import Cliente, Caja, Venta

# Create your views here.

class CajaViewSet(viewsets.ModelViewSet):
    serializer_class = CajaSerializer
    queryset = Caja.objects.all()

class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()

class VentaViewSet(viewsets.ModelViewSet):
    serializer_class = VentaSerializer
    queryset = Venta.objects.all()

class DetalleVenta(viewsets.ModelViewSet):
    serializer_class = VentaSerializer
    queryset = Venta.objects.all()