# application/views/order_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid
from app.models import Order
import json
from app.content.orders import OrdersManager,AnalyticsOrders
from django.http import JsonResponse


class DashboardInfoTimeRealDay(APIView):
  def post(self,request):
      
    try:
        payload= {
            "orders": [],
            "earns": [] ,# ordenes con el estado pagado,
            "customers":[]
        }
        
        data = request.data  # DRF ya parsea el JSON automáticamente

        # if data.get("id"): 
        #     JsonResponse({'id no valida'})
        
        id_business = data.get("id")
        
        #metodo para obtener ordenes
        
        get_list_orders = OrdersManager.get_list_orders_id(idBusiness=id_business) # 
        
        analytics = AnalyticsOrders(get_list_orders)
        response =  analytics.report_by_admin()
        
        #metodo para encontrar todas las ganancias | stado del  orden pagado
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({"error": str(e)})
        
    
    
    
    