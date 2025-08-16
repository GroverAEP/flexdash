# application/views/order_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
from app.models import Order
import json
from app.content.orders import OrdersManager,AnalyticsOrders
from django.http import JsonResponse
from django.shortcuts import redirect
from app.conexion import BDConnection


class PaymentProcess(APIView):
    
    def __init__(self):
        pass
    
    
    def post(self,request):
        
        #o talvez traiga la infomracionc directamente
        try:
            order_json = request.POST.get('order')
            next_url = request.POST.get("next")
            order_data = json.loads(order_json)      # lo conviertes a dict
            print(next_url)
            print(order_data)
            #cambia la informacion , a
            order_data['status'] = "completed"
            
            print(order_data["id"])
            
            order = Order.objects.get(id=order_data["id"])
            order.status = order_data["status"]
            # order.total = order_data["total"]
            # order.date = order_data["date"]
            order.save()      
            # # if id_order:
            
            #deberia de subir los datos al servidor cuando ya esten completados? 
            #deberia de los datos esperarse a que el dia termine para recien subirse al servidor?
            
            
            
            # -- proceso de boleta electronica    
            
            
            # -- proceso subir orden completada la base de datos
            # -- subir a la base de datos cuando termine el dia
             
            # collection, conexion  = BDConnection.conexion_order_mongo()
            
            # result =collection.insert_one(order_data)
            
            # if result.inserted_id:
            #     Order.objects.filter(id= order_data.id).delete()

            
            # conexion.close()

            return redirect("home")   # redirige a la URL con name="home"


            # return JsonResponse({
            #     "response": "orden validad completado"
            # })
        except Exception as e:
            return JsonResponse({"error": str(e)})
    def get(self,request):
        return JsonResponse({"error": "metodo no valido"})