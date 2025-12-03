#!/usr/bin/env python
"""
Script para verificar que los endpoints de Caja están siendo generados correctamente
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mercado.settings')
django.setup()

from rest_framework.routers import DefaultRouter
from sales.views import CajaViewSet

# Crear router y registrar CajaViewSet
router = DefaultRouter()
router.register(r'caja', CajaViewSet, basename='caja')

# Mostrar todas las URLs generadas
print("=" * 60)
print("ENDPOINTS GENERADOS PARA CAJA:")
print("=" * 60)
for url_pattern in router.urls:
    print(f"Pattern: {url_pattern.pattern}")
    if hasattr(url_pattern, 'name'):
        print(f"Name: {url_pattern.name}")
    print("-" * 60)

print("\n✅ Los métodos @action deben generar automáticamente:")
print("  - POST /ventas/api/caja/abrir_caja/")
print("  - POST /ventas/api/caja/{id}/cerrar_caja/")
print("  - GET /ventas/api/caja/obtener_caja_activa/")
