from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from pathlib import Path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('sucursal/', include('sucursal.urls')),
    path('sales/', include('sales.urls')),
]






# Servir archivos media en desarrollo

if settings.DEBUG:
    # Ruta para imagenes desde /products/media/imagenes
    urlpatterns += [
        re_path(r'^media/products/imagenes/(?P<path>.*)$', serve, {
            'document_root': Path(settings.BASE_DIR) / 'media' / 'products' / 'imagenes',
        }),
    ]
    # Ruta general para media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
