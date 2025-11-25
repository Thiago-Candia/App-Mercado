from django.shortcuts import render
from django.db import transaction
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from .serializer import VentasPorMesSerializer, CajaSerializer, VentaSerializer, ClienteSerializer, DetalleVentaSerializer, DescuentoUnitarioSerializer, CobrarSerializer, VentasPorDiaSerializer, DescuentoSerializer
from .models import Cliente, Caja, Venta, DetalleVenta
from decimal import Decimal

class CajaViewSet(viewsets.ModelViewSet):
    serializer_class = CajaSerializer
    queryset = Caja.objects.all()

class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()

class VentaViewSet(viewsets.ModelViewSet):
    serializer_class = VentaSerializer
    queryset = Venta.objects.all()

    @action(detail=True, methods=['post', 'get'], serializer_class=DescuentoSerializer)
    @transaction.atomic
    def hacer_descuento(self, request, pk=Venta.pk):
        venta = self.get_object()
        serializer = DescuentoSerializer(data=request.data)
        
        if serializer.is_valid():
            descuento = serializer.validated_data['descuento']
            descuento_venta = float(venta.calcular_total()) * (descuento / 100)
            total_venta = venta.calcular_total()
            venta.total = float(total_venta) - descuento_venta
            venta.save()
            return Response({'total con descuento' : venta.total, 'descuento' : descuento_venta}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'GET'], serializer_class=CobrarSerializer)
    @transaction.atomic
    def cobrar_venta(self, request, pk=Venta.pk):
        venta = self.get_object()
        if venta.estado_venta == Venta.estadoVenta.FINALIZADA:
            return Response({'error': 'Venta ya cobrada'}, status=400)

        serializer = CobrarSerializer(data=request.data)
        if serializer.is_valid():
            monto_recibido = serializer.validated_data['monto_recibido']
            total_venta = venta.calcular_total()
            descuento = serializer.validated_data['descuento']

            if monto_recibido >= total_venta:
                for detalle in venta.detalles.all():
                    producto = detalle.producto 
                    producto.stock -= detalle.cantidad
                    producto.save()
                venta.total = total_venta
                venta.estado_venta = Venta.estadoVenta.FINALIZADA
                venta.save()
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

        if ventas.count() == 0:
            return Response({'status': 'fecha sin venta'}, status=status.HTTP_204_NO_CONTENT)
        else:
            venta_serializer = self.get_serializer(ventas, many=True)
            detalles = venta_serializer.data
            ventas_count = len(detalles)
            total_dia = sum(venta.calcular_total() for venta in ventas)
            return Response({'fecha': fecha_filtrada, 'cantidad_ventas': ventas_count, 'ventas': detalles, 'total del dia' : total_dia}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get', 'post'], serializer_class=VentasPorMesSerializer)
    def filtra_mes(self, request, pk=None):
        serializer = VentasPorMesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        anio_filtrada = serializer.validated_data['anio_filtrada']
        mes_filtrada = serializer.validated_data['mes_filtrada']
        
        ventas = self.get_queryset().filter(fecha__year=anio_filtrada, fecha__month=mes_filtrada)
        
        if ventas.count() == 0:
            return Response({'status': 'fecha sin venta'}, status=status.HTTP_204_NO_CONTENT)
        

        venta_serializer = self.get_serializer(ventas, many=True)
        detalles = venta_serializer.data
        ventas_count = len(detalles)
        total_mes = sum(venta.calcular_total() for venta in ventas)
        
        return Response({
            'anio': anio_filtrada,
            'mes': mes_filtrada,
            'cantidad_ventas': ventas_count,
            'total_mes': float(total_mes),
            'ventas': detalles
        }, status=status.HTTP_200_OK)

class DetalleVentaViewSet(viewsets.ModelViewSet):
    serializer_class = DetalleVentaSerializer
    queryset = DetalleVenta.objects.all()

