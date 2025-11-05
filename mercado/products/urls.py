
from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()

router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'catalogo', views.CatalogoViewSet, basename='catalogo')
router.register(r'categoria', views.CategoriaViewSet, basename='categoria')
router.register(r'subcategoria', views.SubCategoriaViewSet, basename='subcategoria')

urlpatterns = [
    path('api/', include(router.urls)),
]