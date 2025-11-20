from rest_framework import serializers
from .models import User, Empleado

from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        passsword = validated_data.pop('password')
        user = User(**validated_data)
        user.password = make_password(passsword)
        user.save()
        return user

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