from django.urls import path, re_path
from .views import UserViewSet, register, login
from rest_framework.routers import DefaultRouter
from django.urls import include
from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = [
    path('api/', include(router.urls)),
    re_path('register', views.register),
    re_path('login', views.login)
    ]
