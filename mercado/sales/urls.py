from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()

router.register(r'caja', views.CajaViewSet, basename='caja')
router.register(r'cliente', views.ClienteViewSet, basename='cliente')
router.register(r'venta', views.VentaViewSet, basename='venta')

urlpatterns = [
    path('api/', include(router.urls)),
]