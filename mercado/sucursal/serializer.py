from rest_framework import serializers
from .models import Sucursal, Empleado

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    sucursal = serializers.StringRelatedField(read_only=True)
    sucursal_id = serializers.PrimaryKeyRelatedField(
        queryset=Sucursal.objects.all(),
        source='sucursal',
        write_only=True
    )
    class Meta:
        model = Empleado
        fields ='__all__'




