from django.shortcuts import render
from django.db import transaction
from rest_framework.response import Response
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from .serializer import CajaSerializer, VentaSerializer, ClienteSerializer, DetalleVentaSerializer, CobrarSerializer
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

    @action(detail=True, methods=['post', 'GET'], serializer_class=CobrarSerializer)
    def cobrar_venta(self, request, pk=Venta.pk):
        venta = self.get_object()
        serializer = CobrarSerializer(data=request.data)
        if serializer.is_valid():
            monto_recibido = serializer.validated_data['monto_recibido']
            total_venta = venta.calcular_total()
            if monto_recibido >= total_venta:
                cambio = monto_recibido - total_venta
                return Response({'status': 'pago realizado', 'cambio': cambio}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'pago insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



class DetalleVentaViewSet(viewsets.ModelViewSet):
    serializer_class = DetalleVentaSerializer
    queryset = DetalleVenta.objects.all()