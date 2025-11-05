from django.db import models

# Create your models here.
class Sucursal(models.Model):
    provincia = models.CharField(max_length=50, blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=50)
    contacto = models.CharField(max_length=50)

class Empleado(models.Model):
    class Cargo(models.TextChoices):
        GERENTE = 'GER', 'Gerente'
        EMPLEADO = 'EMP', 'Empleado'

    nombre = models.CharField(max_length=20, blank=False)
    apellido = models.CharField(max_length=20, blank=False)
    dni = models.IntegerField(unique=True, blank=False)
    direccion = models.CharField(max_length=50)
    telefono = models.IntegerField(default='')
    mail = models.CharField(max_length=50)
    cargo = models.CharField(max_length=3, choices=Cargo.choices)
    sucursal = models.ForeignKey(Sucursal, related_name='Empleados', on_delete=models.DO_NOTHING)
    contratoPrincipio = models.DateField()
    contratoFin = models.DateField()



