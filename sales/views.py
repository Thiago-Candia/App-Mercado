from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializer import CajaSerializer, VentaSerializer, ClienteSerializer, DetalleVentaSerializer
from .models import Cliente, Caja, Venta, DetalleVenta

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


class DetalleVentaViewSet(viewsets.ModelViewSet):
    serializer_class = DetalleVentaSerializer
    queryset = DetalleVenta.objects.all()