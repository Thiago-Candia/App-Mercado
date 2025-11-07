from django.contrib import admin
from .models import Product, Catalogo, CategoriaProducto, SubCategoriaProducto

# Register your models here.


admin.site.register(Product)
admin.site.register(Catalogo)
admin.site.register(CategoriaProducto)
admin.site.register(SubCategoriaProducto)