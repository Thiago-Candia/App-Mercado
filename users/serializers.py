from rest_framework import serializers
from .models import User, Empleado

class UserSerializer(serializers.ModelSerializer):
    empleado = serializers.StringRelatedField(read_only=True)
    empleado_id = serializers.PrimaryKeyRelatedField(
    queryset=Empleado.objects.all(),
    source='empleado',
    write_only=True
    )
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }

class UserGetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password"]
        extra_kwargs= {
            "password": {"read_only": True}
        }