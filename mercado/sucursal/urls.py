
from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()

router.register(r'sucursal', views.SucursalViewSet, basename='sucursal')
router.register(r'empleado', views.EmpleadoViewSet, basename='empleado')

urlpatterns = [
    path('api/', include(router.urls)),
]