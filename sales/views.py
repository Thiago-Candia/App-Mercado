from django.shortcuts import render
from django.db import transaction
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from .serializer import VentasPorMesSerializer, CajaSerializer, VentaSerializer, ClienteSerializer, DetalleVentaSerializer, DescuentoUnitarioSerializer, CobrarSerializer, VentasPorDiaSerializer, DescuentoSerializer
from .models import Cliente, Caja, Venta, DetalleVenta
from decimal import Decimal
from datetime import date
from django.utils import timezone
from django.conf import settings




class CajaViewSet(viewsets.ModelViewSet):
    serializer_class = CajaSerializer
    queryset = Caja.objects.all()



    @action(detail=False, methods=['post'])
    def abrir_caja(self, request):
        """
        POST /ventas/api/caja/abrir_caja/
        Body: { "empleado_id": 1, "numeroCaja": 1 }
        """
        empleado_id = request.data.get('empleado_id')
        numero_caja = request.data.get('numeroCaja')
        
        if not empleado_id or not numero_caja:
            return Response(
                {'error': 'Se requieren empleado_id y numeroCaja'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Verificar si ya existe una caja activa para este empleado
            caja_activa = Caja.objects.filter(
                empleado_id=empleado_id,
                estado='ACT'
            ).first()
            
            if caja_activa:
                return Response(
                    {'error': f'Empleado ya tiene caja activa: {caja_activa.numeroCaja}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # buscar o crear la caja y obtener hora actual en la zona horaria configurada
            ahora = timezone.now()
            hora_argentina = ahora.astimezone(timezone.get_current_timezone()).time()
            
            caja, created = Caja.objects.get_or_create(
                numeroCaja=numero_caja,
                empleado_id=empleado_id,
                defaults={
                    'estado': 'ACT',
                    'apertura': hora_argentina
                }
            )
            
            if not created:
                # Si ya existe, activarla
                ahora = timezone.now()
                hora_argentina = ahora.astimezone(timezone.get_current_timezone()).time()
                caja.estado = 'ACT'
                caja.apertura = hora_argentina
                caja.cierre = None
                caja.save()
            
            serializer = CajaSerializer(caja)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



    @action(detail=True, methods=['post'])
    def cerrar_caja(self, request, pk=None):
        """
        POST /ventas/api/caja/{id}/cerrar_caja/
        Body: {}
        """
        caja = self.get_object()
        
        if caja.estado == 'CER':
            return Response(
                {'error': 'La caja ya está cerrada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Obtener hora actual en la zona horaria configurada
        ahora = timezone.now()
        hora_argentina = ahora.astimezone(timezone.get_current_timezone()).time()
        
        caja.estado = 'CER'
        caja.cierre = hora_argentina
        caja.save()
        
        serializer = CajaSerializer(caja)
        return Response(serializer.data, status=status.HTTP_200_OK)



    @action(detail=False, methods=['get'])
    def obtener_caja_activa(self, request):
        """
        GET /ventas/api/caja/obtener_caja_activa/
        Retorna la caja activa del empleado actual
        """
        empleado_id = request.query_params.get('empleado_id')
        
        if not empleado_id:
            return Response(
                {'error': 'Se requiere empleado_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        caja = Caja.objects.filter(
            empleado_id=empleado_id,
            estado='ACT'
        ).first()
        
        if not caja:
            return Response(None, status=status.HTTP_200_OK)
        
        serializer = CajaSerializer(caja)
        return Response(serializer.data, status=status.HTTP_200_OK)



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
            return Response({'error': 'Venta ya cobrada'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CobrarSerializer(data=request.data)
        if serializer.is_valid():
            monto_recibido = serializer.validated_data['monto_recibido']
            total_venta = venta.calcular_total()
            descuento = serializer.validated_data.get('descuento', 0)

            if monto_recibido >= total_venta:
                # Obtener detalles de venta usando DetalleVenta
                detalles = DetalleVenta.objects.filter(venta=venta)
                for detalle in detalles:
                    producto = detalle.producto 
                    producto.stock -= detalle.cantidad
                    producto.save()

                venta.total = total_venta
                venta.estado_venta = Venta.estadoVenta.FINALIZADA
                venta.save()

                cambio = monto_recibido - total_venta
                serializer = VentaSerializer(venta)
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

