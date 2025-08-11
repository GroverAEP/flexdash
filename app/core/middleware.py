from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from datetime import datetime
from app.conexion import BDConnection
from app.content.orders import OrdersManager

class LoginRequiredMiddleware:
    """
    Middleware que redirige a LOGIN_URL si el usuario no está autenticado,
    excepto en rutas públicas definidas en `PUBLIC_PATHS`.

    Durante desarrollo, también permite autenticación por Bearer Token estático.
    """
    # Token de prueba para desarrollo (en producción debe ser dinámico y con expiración)
    TOKEN_BEARER = "eXJ3bGciOiJIU2I1NiIsInR4cCI6Ik1XVCJ9.ey5h"

    # Rutas que serán accesibles sin autenticación
    PUBLIC_PATHS = [
        reverse('login'),      # vista de login
        # reverse('register'),   # vista de registro
        '/admin/login/',       # login del admin
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        auth_header = request.headers.get("Authorization", "")

        # Si el header empieza con "Bearer " y el token es correcto
        if auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
            if token == self.TOKEN_BEARER:
                return self.get_response(request)
            
            # elif token is UserNormal
            
            else:
                return JsonResponse({"error": "Bearer token inválido"}, status=401)

        # Si no es un usuario autenticado y no está en rutas públicas → redirigir
        if isinstance(request.user, AnonymousUser) and path not in self.PUBLIC_PATHS:
            return redirect(reverse('login'))

        return self.get_response(request)
    
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

        print(path)
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith('/business/'):
            # Si viene business_id en POST, guardarlo en sesión
            if request.method == "POST":
                business_id = request.POST.get("business_id")
                list_business = request.session.get('business')
                if list_business:
                    negocio = next((b for b in list_business if str(b.get('id')) == str(business_id)), None)
                    request.session['unique_business'] = negocio
                    print(negocio)
                    request.session['unique_business']["status"] = self.setStatusTime(open_time=negocio["time_zone"]["time_open"], close_time=negocio["time_zone"]["time_close"])
                    request.session['unique_business']["orders"] = self.get_list_orders(idBusiness=negocio["id"])
        else:
            # Si no estás en /business/, borrar business_id de sesión
            if 'unique_business' in request.session:
                del request.session['unique_business']

        response = self.get_response(request)
        return response
    # def g etOrdersBusiness(self,idBusiness,):
        
    #     from services.analytics import AnalyticsOrders
    #     AnalyticsOrders.get
    
    def get_list_orders(self,idBusiness:str):
       return OrdersManager.get_list_orders(idBusiness=idBusiness),
    
      
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
        
        OrdersManager.get_list_orders()
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