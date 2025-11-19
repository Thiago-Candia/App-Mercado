from django.shortcuts import render
from django.db import transaction
from rest_framework.response import Response
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from .serializer import CajaSerializer, VentaSerializer, ClienteSerializer, DetalleVentaSerializer, CobrarSerializer, VentasPorDiaSerializer
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
        
    @action(detail=False, methods=['get','POST'], serializer_class=VentasPorDiaSerializer)
    def filtrar_ventas(self, request, pk=None):
        serializer = VentasPorDiaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        fecha_filtrada = serializer.validated_data['fecha_filtrada']
        ventas = self.get_queryset().filter(fecha=fecha_filtrada)
        if ventas.exists():
            venta_serializer = self.get_serializer(ventas, many=True)
            ventas_list = venta_serializer.data
            ventas_count = len(ventas_list)
            ventas_total = sum(venta['total'] for venta in ventas_list)
            return Response({'fecha': fecha_filtrada, 'cantidad_ventas': ventas_count, 'total_ventas': ventas_total, 'ventas': venta_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'fecha sin venta'}, status=status.HTTP_204_NO_CONTENT)

        if ventas.count() == 0:
            return Response({'status': 'fecha sin venta'}, status=status.HTTP_204_NO_CONTENT)
        else:
            venta_serializer = self.get_serializer(ventas, many=True)
            info = venta_serializer.data
            detalles = venta_serializer.data
            ventas_list = venta_serializer.data
            ventas_count = len(ventas_list)

            return Response({'fecha': fecha_filtrada, 'cantidad_ventas': ventas_count, 'ventas': detalles}, status=status.HTTP_200_OK)
    
class DetalleVentaViewSet(viewsets.ModelViewSet):
    serializer_class = DetalleVentaSerializer
    queryset = DetalleVenta.objects.all()


