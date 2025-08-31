# application/views/order_views.py

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings

import uuid
from app.models import Order
import json
from app.content.orders import OrdersManager,AnalyticsOrders
from django.http import JsonResponse
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from app.auth import AuthContent


class LoginView(APIView):
  permission_classes = []  # 👈 así se hace en clase
  authentication_classes = []

  def post(self,request):
    try:
     # form = UserCreationForm(request.POST)
        # print(form)
        
        data = json.loads(request.body)      
        username =data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        print(username)
        print(password)     
        
        # 👇 Forzar que Django guarde la sesión en DB/cache
        # request.session.save()
        if user is not None:
        # Generar tokens JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)    


            
            
            login(request,user)
            
            print("🔑 Session Key:", request.session.session_key)
            # session_key = request.session.session_key
            request.session["access-token"] = str(access_token)   # ya es string
            request.session["refresh-token"] = str(refresh)       # 👈 conviértelo a string
          
                    # 🔑 fuerza a que se guarde la sesión
            # request.session.modified = True
            # request.session.save()
            messages.success(request, "Inicio de sesion exitoso")
            
            response = JsonResponse({
                "token": access_token,
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
                "message": "Inicio de sesion exitoso"
            }, status=200)
            # 🔑 Agregar cookie sessionid correctamente
            response.set_cookie(
                key='sessionid',
                value=request.session.session_key,
                httponly=True,       # JS no puede acceder (seguridad)
                samesite='Lax',     # necesario para cross-origin
                secure=not settings.DEBUG,        # desarrollo HTTP; en producción debe ser True
                path='/',            # obligatorio
                max_age=3600         # duración de la cookie en segundos
            )

            print(response.content)  # bytes, contiene JSON

            print("\nCabeceras que se enviarán:")
            for k, v in response.items():  # headers
                print(k, ":", v)

            print("\nCookies que se enviarán:")
            print(response.cookies)  # Muestra todas las cookies del response

            
            # Body (contenido JSON en bytes)
            print("Body de la respuesta (bytes):")
            print(response.content)

            # Body decodificado (texto JSON legible)
            print("\nBody de la respuesta (JSON):")
            print(response.content.decode('utf-8'))

            # Headers
            print("\nHeaders que se enviarán:")
            for k, v in response.items():
                print(k, ":", v)

            # Cookies
            print("\nCookies que se enviarán:")
            for key, morsel in response.cookies.items():
                print(f"{key} -> {morsel.value}; {morsel.output()}")
            return response
        else:
            messages.error(request,"Usuario o contraseña incorrectos")
            return JsonResponse( {
                "error": "usuario o contraseña incorrectos" }, status = 401)
    except Exception as e:
            return JsonResponse({"error": e})

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]  # 🔒 Solo usuarios autenticados

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
           
        }
        return JsonResponse(data, status=200)
    
    
    
    
    
    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try :
            if request.user:
                logout(request)
                return JsonResponse({
                    "tag":"close",
                    "message": "usuario salio exitosamente"})
            return JsonResponse({
                "tag":"close",
                "message": "no sesion iniciada de usuario "}
            )
        except:
            JsonResponse({"tag":"open", "message": "sesion sigue iniciada"})