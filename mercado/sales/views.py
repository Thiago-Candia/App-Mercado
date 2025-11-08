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

    @action(detail=True, methods=['post'])
    def agregar_producto(self, request, pk=None):
        venta = self.get_object()
        producto_id = request.data.get("producto_id")
        cantidad = int(request.data.get("cantidad", 1))
        
        producto = Product.objects.get(id=producto_id)

        detalle = DetalleVenta.objects.create(venta=venta, producto=producto, cantidad=cantidad)
        detalle.save()

        return self.retrieve(request)

class DetalleVenta(viewsets.ModelViewSet):
    serializer_class = VentaSerializer
    queryset = Venta.objects.all()