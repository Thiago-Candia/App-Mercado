
from time import time
from django.shortcuts import render
from django.db import transaction
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from .serializer import VentasPorMesSerializer, CajaSerializer, CajaAperturaSerializer, CajaCierreSerializer, IngresarEmpleadoCajaSerializer, VentaSerializer, ClienteSerializer, DetalleVentaSerializer, DescuentoUnitarioSerializer, CobrarSerializer, VentasPorDiaSerializer, DescuentoSerializer
from .models import Cliente, Caja, Venta, DetalleVenta
from decimal import Decimal
from datetime import date
from datetime import datetime

class CajaViewSet(viewsets.ModelViewSet):
    serializer_class = CajaSerializer
    queryset = Caja.objects.all()
    @action(detail=True, methods=["get", "post"], serializer_class=CajaAperturaSerializer)
    def caja_apertura(self, request, pk=Caja.id):
        serializer = CajaAperturaSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        caja = self.get_object()
        apertura = date.today()
        caja.fecha = apertura
        caja.apertura = datetime.now().replace(microsecond=0).time()
        caja.estado = 'ACT'
        monto_apertura = serializer.validated_data["monto_apertura"]
        monto_retirado = serializer.validated_data["monto_retirado"]
        caja.save()
        if monto_retirado > 0:
            if monto_retirado > monto_apertura:
                raise({"monto ingresado a retirar superiro al ingreso de caja"}, serializer.errors)
            else:
                monto_apertura = monto_apertura - monto_retirado
                caja.save()
        return Response({'fecha apertura' : apertura, 'hora apertura' : caja.apertura.strftime("%H:%M"), 'monto apertura' : monto_apertura, 'monto_retirado' : monto_retirado })

    @action(detail=True, methods=["get", "post"], serializer_class=CajaCierreSerializer)
    def caja_cierre(self, request, pk=Caja.id):
        serializer = CajaCierreSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        caja = self.get_object()
        cierre = date.today()
        caja.fecha = cierre
        caja.cierre = datetime.now().replace(microsecond=0).time()
        caja.estado = 'CER'
        monto_cierre = serializer.validated_data["monto_cierre"]
        monto_retirado = serializer.validated_data["monto_retirado"]
        caja.save()
        if monto_retirado > 0:
                monto_cierre = monto_cierre - monto_retirado
                caja.save()
        registro_cierre = {
            "fecha": str(cierre),
            "hora_cierre": caja.cierre.strftime("%H:%M"),
            "empleado": str(caja.empleado),
            "monto_cierre": str(monto_cierre),
            "monto_retirado": str(monto_retirado)
        }
        if caja.historial_cierres is None:
            caja.historial_cierres = []
            
        caja.historial_cierres.append(registro_cierre)
        caja.save()
        return Response({'fecha cierre' : cierre, 'hora cierre' : caja.cierre.strftime("%H:%M"), 'monto cierre' : monto_cierre, 'monto_retirado' : monto_retirado })

    @action(detail=True, methods=["get"])
    def historial(self, request, pk=Caja.pk):
        caja = self.get_object()
        return Response({
            'numeroCaja': caja.numeroCaja,
            'historial_cierres': caja.historial_cierres
        })

    @action(detail=True, methods=['get','post'], serializer_class=IngresarEmpleadoCajaSerializer)
    def ingresar_empleado_caja(self, request, pk=Caja.pk):
        serializer = IngresarEmpleadoCajaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        empleado= serializer.validated_data["empleado"]
        caja = self.get_object()
        caja.empleado = empleado
        caja.save()
        return Response({'empleado' : str(empleado), 'caja': str(caja)}, status=status.HTTP_200_OK)

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
            if (descuento <= 0) or (descuento > 100):
                return Response({"monto de descuento invalido" : descuento}, status=status.HTTP_400_BAD_REQUEST)
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
        venta.estado_venta = Venta.estadoVenta.EN_PROCESO
        serializer = CobrarSerializer(data=request.data)
        if serializer.is_valid():
            monto_recibido = serializer.validated_data['monto_recibido']
            total_venta = venta.calcular_total()
                
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
        metodo_pago = serializer.validated_data['metodo_pago']
        ventas = self.get_queryset().filter(fecha=fecha_filtrada, metodo_pago=metodo_pago)

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
        metodo_pago = serializer.validated_data['metodo_pago']
        ventas = self.get_queryset().filter(fecha__year=anio_filtrada, fecha__month=mes_filtrada, metodo_pago=metodo_pago)

        if (mes_filtrada < 1) or (mes_filtrada > 12):
            return Response({'status': 'mes invalido'}, status=status.HTTP_400_BAD_REQUEST)

        if (anio_filtrada > 3000) and (anio_filtrada < 1):
            return Response({'status': 'ano invalido'}, status=status.HTTP_400_BAD_REQUEST)
        
        if ventas.count() == 0:
            return Response({'status': 'mes sin venta'}, status=status.HTTP_204_NO_CONTENT)

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

