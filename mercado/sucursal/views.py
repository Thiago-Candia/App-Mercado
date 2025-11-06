from django.shortcuts import render
from rest_framework import viewsets
from .serializer import EmpleadoSerializer, SucursalSerializer
from .models import Empleado, Sucursal

class SucursalViewSet(viewsets.ModelViewSet):
    serializer_class = SucursalSerializer
    queryset = Sucursal.objects.all()

class EmpleadoViewSet(viewsets.ModelViewSet):
    serializer_class = EmpleadoSerializer
    queryset = Empleado.objects.all()