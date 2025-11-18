import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sucursal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='CatalogoProductos', to='sucursal.sucursal')),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('catalogo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Categoria', to='products.catalogo')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategoriaProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Subcategoria', to='products.catalogo')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('codigo', models.IntegerField()),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/imagenes')),
                ('stock', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Producto', to='products.categoriaproducto')),
                ('subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Producto', to='products.subcategoriaproducto')),
            ],
        ),
    ]
