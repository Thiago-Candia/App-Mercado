from django.contrib import admin
from .models import Cliente, Caja, Venta

# Register your models here.

admin.site.register(Cliente)
admin.site.register(Caja)
admin.site.register(Venta)