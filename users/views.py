from rest_framework import viewsets, status
from .serializers import UserSerializer, UserGetPasswordSerializer
from .models import User, Empleado
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view
from rest_framework.views import APIView as API
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


""" TOKENS PARA USUARIOS (verificacion) """
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


@api_view(['POST'])
def register(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': serializer.data
                })
        else:
                return Response(serializer.errors, status=404)
        

@api_view(['POST'])
def login(request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
                return Response({"error": "Credenciales inválidas"}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
        })


class UserViewSet(viewsets.ModelViewSet):
        serializer_class = UserSerializer
        queryset = User.objects.all()
        @action(detail=True, methods=["GET"], serializer_class=UserGetPasswordSerializer)
        def get_password(self, request, pk=User.pk):
                user = self.get_object()
                serializer = UserGetPasswordSerializer(data=request.data)
                if not serializer.is_valid():
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                password_user = user.get_password()
                return Response({'usuario': user.username, 'contrasena' : password_user}, status=status.HTTP_200_OK)
