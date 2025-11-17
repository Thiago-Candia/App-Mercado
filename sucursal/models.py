from django.db import models
from .validaciones import pedir_dni_hasta_valido, pedir_mail_hasta_valido, pedir_nombre_hasta_valido, pedir_telefono_hasta_valido
# Create your models here.
class Sucursal(models.Model):
    provincia = models.CharField(max_length=50, blank=False, null=False)
    ciudad = models.CharField(max_length=50, blank=False, null=False)
    direccion = models.CharField(max_length=50, blank=False, null=False)
    nombre = models.CharField(max_length=50)
    contacto = models.IntegerField(max_length=50)
    mail = models.EmailField(blank=False, validators=[pedir_mail_hasta_valido])
    
    def __str__(self):
        return f"{self.nombre.upper()} {self.ciudad} {self.direccion}"

class Empleado(models.Model):
    class Cargo(models.TextChoices):
        GERENTE = 'GER', 'Gerente'
        EMPLEADO = 'EMP', 'Empleado'

    nombre = models.CharField(max_length=20, blank=False, validators=[pedir_nombre_hasta_valido])
    apellido = models.CharField(max_length=20, blank=False, validators=[pedir_nombre_hasta_valido])
    dni = models.IntegerField(unique=True, blank=False, validators=[pedir_dni_hasta_valido])
    direccion = models.CharField(max_length=50)
    telefono = models.IntegerField(blank=True, validators=[pedir_telefono_hasta_valido])
    mail = models.EmailField(max_length=50, validators=[pedir_mail_hasta_valido])
    cargo = models.CharField(max_length=3, choices=Cargo.choices)
    contratoPrincipio = models.DateField()
    contratoFin = models.DateField()
    sucursal = models.ForeignKey(Sucursal, related_name='Empleados', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"""NOMBRE: {self.apellido.upper()} {self.nombre.upper()} - DNI: {self.dni} - SUCURSAL: {self.sucursal}"""



