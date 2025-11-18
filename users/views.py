from rest_framework import viewsets, status
from .serializers import UserSerializer, UserGetPasswordSerializer
from .models import User, Empleado
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view
from rest_framework.views import APIView as API
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

@api_view(['POST'])
def login(request):
        username = request.data.get('username')
        password = request.data.get('password')
        

        if not username or not password:
                return Response({"error": "username y password son requeridos"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)


        if user is None:
                return Response(
                {"error": "Credenciales inválidas"},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)

        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
        empleado_id = request.data.get('empleado_id')

        empleado = Empleado.objects.get(id=empleado_id)
        usuario_existente = User.objects.filter(empleado=empleado).first()
        if usuario_existente:
                return Response({
                "error": "Ya existe un usuario para este empleado",
                "username_existente": usuario_existente.username,
                "user_id": usuario_existente.id }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
                user = User()
                user.set_empleado(empleado)
                user.save()

                token = Token.objects.create(user=user)
                return Response({'token': token.key, "user" : serializer.data}, status=status.HTTP_201_CREATED)
        else:
                return Response({"status": "usuario existe"}, status=status.HTTP_400_BAD_REQUEST)



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
