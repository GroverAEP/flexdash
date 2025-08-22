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
from django.utils import timezone


class PaymentProcess(APIView):
    
    def __init__(self):
        pass
    
    
    def post(self,request):
        
        #o talvez traiga la infomracionc directamente
        try:
            
            
            order_json = request.POST.get('order')
            next_url = request.POST.get("next")
            order_data = json.loads(order_json)      # lo conviertes a dict
           
            OrdersManager.validated_order_process(id_order=order_data["id"] , data=order_data)


            return JsonResponse({"redirect": next_url})


            # return JsonResponse({
            #     "response": "orden validad completado"
            # })
        except Exception as e:
            return JsonResponse({"error": str(e)})
    def get(self,request):
        return JsonResponse({"error": "metodo no valido"})
    

class PaymentCancelled(APIView):
    def post(self,request):
            
        try:
            order_json = request.POST.get('order')
            next_url = request.POST.get("next")
            
            reason = request.POST.get("reason")
            
            order_data = json.loads(order_json)      # lo conviertes a dict 
            

            # actualizamos la orden
            # order = Order.objects.get(id=order_data["id"])
            # order.status = order_data["status"]
            # order.carts = carts
            # order.save()
            OrdersManager.cancelled_order_process(id_order=order_data["id"] , data=order_data,reason=reason)

                        
            
            # order_json["reason"] = {}
            # guardo como prueab
            
            #actualiza la orden el objeto
            order = Order.objects.get(id=order_data["id"])
            order.status = order_data["status"]
            order.carts = order_data["carts"]["reason"]
            # order.date = order_data["date"]
            order.save()
            
            
            return redirect(next_url)
        except Exception as e:
            return JsonResponse({"error": str(e)})