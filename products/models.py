from django.db import models
from sucursal.models import Sucursal

class Catalogo(models.Model):
    name = models.CharField(max_length=100, default='Catalogo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sucursal = models.ForeignKey(Sucursal, related_name='CatalogoProductos', on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name

class CategoriaProducto(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    catalogo = models.ForeignKey(Catalogo, related_name='Categoria', on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name

class SubCategoriaProducto(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey(CategoriaProducto, related_name='Subcategoria', on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    codigo = models.IntegerField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/imagenes', null=True, blank=True)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey(CategoriaProducto, related_name='productos', on_delete=models.DO_NOTHING) 
    subcategoria = models.ForeignKey(SubCategoriaProducto, related_name='productos', on_delete=models.DO_NOTHING, blank=True)
    
    @property   
    def precio_formateado(self):
        return f"${self.price:,.2f}"
    
    @property
    def esta_disponible(self):
        return self.stock > 0 and f'{self.stock}'
    
    def __str__(self):
        return f'{self.name} {self.precio_formateado}'