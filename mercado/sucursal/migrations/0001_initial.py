import django.db.models.deletion
import sucursal.validaciones
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provincia', models.CharField(blank=True, max_length=50, null=True)),
                ('ciudad', models.CharField(blank=True, max_length=50, null=True)),
                ('direccion', models.CharField(blank=True, max_length=50, null=True)),
                ('nombre', models.CharField(max_length=50)),
                ('contacto', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, validators=[sucursal.validaciones.pedir_nombre_hasta_valido])),
                ('apellido', models.CharField(max_length=20, validators=[sucursal.validaciones.pedir_nombre_hasta_valido])),
                ('dni', models.IntegerField(unique=True, validators=[sucursal.validaciones.pedir_dni_hasta_valido])),
                ('direccion', models.CharField(max_length=50)),
                ('telefono', models.IntegerField(default='', validators=[sucursal.validaciones.pedir_telefono_hasta_valido])),
                ('mail', models.CharField(max_length=50, validators=[sucursal.validaciones.pedir_telefono_hasta_valido])),
                ('cargo', models.CharField(choices=[('GER', 'Gerente'), ('EMP', 'Empleado')], max_length=3)),
                ('contratoPrincipio', models.DateField()),
                ('contratoFin', models.DateField()),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Empleados', to='sucursal.sucursal')),
            ],
        ),
    ]
