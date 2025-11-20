from django.db import models
from sucursal.models import Empleado
from rest_framework import serializers
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from .managers import UserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    empleado =models.OneToOneField(Empleado, on_delete=models.CASCADE, related_name='user')
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    password = models.CharField(max_length=128)  
    class Admin(models.TextChoices):
        ADMIN = 'ADM', 'Administrador'
        CAJERO = 'CAJ', 'Cajero'
    admin = models.CharField(max_length=3, choices=Admin.choices, default=Admin.CAJERO)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    def set_admin(self, is_admin):
        if self.empleado.cargo == 'GER':
            self.admin = self.Admin.ADMIN
        else:
            self.admin = self.Admin.CAJERO


    def set_empleado(self, nuevo_empleado):
        self.empleado = nuevo_empleado
        return self.empleado

    def save(self, *args, **kwargs):
        try:
            if not self.username and not self.password:
                self.username = self.empleado.dni
                raw_password = self.empleado.nombre.lower() + self.empleado.apellido.lower()
                self.password = make_password(raw_password)
            super().save(*args, **kwargs)
        except:
            raise serializers.ValidationError(f"usuario con DNI{self.username} ya existe")

    def get_password(self):
        return f'{self.password}'


    def __str__(self):
        return self.username