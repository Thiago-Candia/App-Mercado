

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sucursal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=20)),
                ('dni', models.IntegerField(blank=True)),
                ('metodo_pago', models.CharField(choices=[('EFE', 'Efectivo'), ('CRE', 'Credito'), ('DEB', 'Debito'), ('TRA', 'Transferencia')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeroCaja', models.IntegerField()),
                ('estado', models.CharField(choices=[('ACT', 'Activa'), ('CER', 'Cerrada')], max_length=3)),
                ('empleado', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='sucursal.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('caja', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='sales.caja')),
                ('cliente', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='sales.cliente')),
            ],
        ),
    ]
