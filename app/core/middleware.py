from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from datetime import datetime
from app.conexion import BDConnection
from app.content.orders import OrdersManager
from app.content.business import BusinessManager
from app.content.admin import AdminContent
from rest_framework_simplejwt.tokens import AccessToken
from app.models import User  # importa tu modelo real

class LoginRequiredMiddleware:
    """
    Middleware para proteger rutas excepto las públicas.
    Usa token Bearer estático para autenticación (solo desarrollo).
    Devuelve 401 JSON en vez de redirigir para que el frontend maneje el login.
    """

    TOKEN_BEARER = "eXJ3bGciOiJIU2I1NiIsInR4cCI6Ik1XVCJ9.ey5h"

    PUBLIC_PATHS = [
        '/api/public/',    # rutas públicas de API
        # '/api/auth/login/',     # login en backend (si existiera)
        # '/api/profile/',
        '/api/validated/'
        '/api/cancelled/'
        '/api/dashboard/validate/',  
        '/api/get_info_client/'     
        # agrega otras rutas públicas que quieras permitir
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        auth_header = request.headers.get("Authorization", "")
        access_token = request.session.get("access-token")

        request.session.get("access-token")
        print(access_token)
        print(request.headers.get("Authorization"))
        
        print("paso por midleware")
        print(request.user)
        
        
        # if request.user.is_authenticated:
        #     print("autentificado")
        #     return self.get_response(request)
        # Si la ruta es pública, permite sin autenticación
        if not any(path.startswith(p) for p in self.PUBLIC_PATHS):
            print("asdsad")
            return self.get_response(request)

        # Verifica token Bearer
        if auth_header.startswith("Bearer "):
            print("No")
            token = auth_header.split("Bearer ")[1]
            if token == self.TOKEN_BEARER:
                # Aquí podrías asignar un user ficticio si quieres
                return self.get_response(request)
            else:
                return JsonResponse({"error": "Token inválido"}, status=401)

        #autentificacion por medio de inicio sesion en navegador
        elif request.session.get("access-token"):
            print("access-tok")
            try:
                print(access_token)
                token = AccessToken(access_token)  # ✅ valida firma y expiración
                user_id = token["user_id"]          # sacas el claim
                user = User.objects.get(id=user_id)
                request.user = user
                
                # responseAdmin = AdminContent.get_user_id(id=str(request.user.profile.id_profile  ))
                # responseBusiness = BusinessManager.get_list_business_id(idAdmin=str(request.user.profile.id_profile))
                # print(responseBusiness)
                print("✅ Usuario autenticado:", user)
                print("✅ Usuario request:", request.user)
                print("usuario de administrador:" , request.session["user"]["full_name"])
                # print("negocios del administrador:" ,responseBusiness)

                return self.get_response(request)
            
            except Exception as e:
                print("❌ Token de sesión inválido:", str(e))
                return JsonResponse({"error": "Token de sesión inválido"}, status=401)
        else:
            print("paso aca")
            # Si no hay token ni está autenticado, devuelve 401
            if isinstance(request.user, AnonymousUser):
                return JsonResponse({"error": "No autenticado"}, status=401)

class BusinessSessionMiddleware:
    """
    Middleware para mantener business_id en sesión
    solo dentro de ciertas rutas y eliminarlo si sale de ellas.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Define las rutas o prefijos donde quieres mantener el dato
        
        self.allowed_paths = [
            '/dashboard/',
            '/preorders/',
            '/options/',
        ]


    def __call__(self, request):
        path = request.path
        
        print(request.session.get("access-token"))
        
          # Si ya existe en sesión, no hacemos nada

        if request.session.get("unique_business"):
            print("existe_ unique _:busniess")
            return self.get_response(request)
        
        if path.startswith('/business/'):
           
           
            # Si viene business_id en POST, guardarlo en sesión
           
            print("llamado al midleware")
            print("si no existe business_id")
            business_id = None
            if request.method == "POST":
                business_id = request.POST.get("business_id")
            elif request.method == "GET":
                print(business_id)
                business_id = request.GET.get("business_id")
                print(business_id)

            # Si viene un ID nuevo, lo guardamos en sesión
            if business_id:
                print("llamado - guardo sesion")
                list_business = request.session.get('business')
                if list_business:
                    #encuentro el negocio por id
                    negocio = BusinessManager.get_business_id(idBusiness=business_id)
                    print(negocio)
                    # negocio = next((b for b in list_business if str(b.get('id')) == str(business_id)), None)
                    if negocio:
                        print("guardamos el negocio en sesion")
                        request.session['unique_business'] = negocio
                        # print(negocio.get(["time_zone"],"noexiste"))
                        request.session['unique_business']["status"] = self.setStatusTime(
                            open_time=negocio["time_zone"]["time_open"],
                            close_time=negocio["time_zone"]["time_close"]
                        )
                        request.session['unique_business']["orders"] = self.get_list_orders(
                            idBusiness=negocio["id"]
                        )

            # Si estás en una de las rutas permitidas y ya hay negocio en sesión, recarga datos
            elif path in self.allowed_paths and 'unique_business' in request.session:
                print("recarga de datos")
                negocio = request.session['unique_business']
                request.session['unique_business']["status"] = self.setStatusTime(
                    open_time=negocio["time_zone"]["time_open"],
                    close_time=negocio["time_zone"]["time_close"]
                )
                request.session['unique_business']["orders"] = self.get_list_orders(
                    idBusiness=negocio["id"]
                )

        # Si sales de las rutas permitidas, borramos
        elif 'unique_business' in request.session:
            del request.session['unique_business']

        response = self.get_response(request)
        return response
    # def g etOrdersBusiness(self,idBusiness,):
        
    #     from services.analytics import AnalyticsOrders
    #     AnalyticsOrders.get
    
    def get_list_orders(self,idBusiness:str):
              return OrdersManager.get_list_orders_id(idBusiness=idBusiness)

      
    @classmethod  
    def setStatusTime(self, open_time: str, close_time: str):
        # Obtener la hora actual
        now = datetime.now().time()

        # Convertir strings a objetos time
        open_time = datetime.strptime(open_time, "%H:%M:%S").time()
        close_time = datetime.strptime(close_time, "%H:%M:%S").time()

        # Validar si está abierto o cerrado
        if open_time <= now <= close_time:
            return "abierto"
        else:
            
            #cargar los datos, una vez que el negocio cierre
            # self.set_orders_business(self.)
            return "cerrado"
    
      
     
     
    @classmethod
    def set_orders_business(self):
        
        #Obtener la bd  
        collection, conexion = BDConnection.conexion_order_mongo()
        
        OrdersManager.get_list_orders_id()
        #unico archivo con cada una de las ordenes de un negocio
        {
            "id_business": "",
            "close_time":"",
            "orders":[]
        }
        orders = [
                    {
            "id_business": "",
            "close_time":"",
            "orders":[]
        },        
        {
            "id_business": "",
            "date_close":"",
            "orders":[
                
                {
                    "id_business":"",
                    "id_client":"",
                    "id_orders":"",
                    "data":{},
                    "date":"1-2-3-2",
                    
                }
            ]
        }
        ##get-> Visualizarlo en el backend
        # set-> Orders
        # get-> Orders
        
                    ] 
        
        #unico archivo con un solo dato - repite el mismo id_business en cada agrgado
        {
            "id_business":"",
            "id_client":"",
            "id_orders":"",
            "data":{},
            "date":"1-2-3-2",
            
        }
        
        #unico archivo con solo un dato para el cliente- cada cliente un numero de ordenes,
        
        {
            "id_client": "",
            "close_time":"",
            "orders":[]
        }
        
        collection.insert_many()
        
        
        conexion.close()
        
        
        

















import threading

_thread_locals = threading.local()

def get_current_request():
    return getattr(_thread_locals, "request", None)

class ThreadLocalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        response = self.get_response(request)
        return response