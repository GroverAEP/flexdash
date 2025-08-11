# application/views/order_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
from app.models import Order
import json
from app.content.orders import OrdersManager,AnalyticsOrders
from django.http import JsonResponse

class OrderCreateAPIView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            # uuid.UUID(data.get("idBusiness")) if data.get("idBusiness") else uuid.uuid4()
            # uuid.UUID(data.get("idClient")) if data.get("idClient") else uuid.uuid4()
            id_business = data.get("idBusiness") if data.get("idBusiness") else uuid.uuid4()
            id_client = data.get("idClient") if data.get("idClient") else uuid.uuid4()
            carts=data.get("carts", {})
            total_amount=data.get("total_amount")
            
            response = OrdersManager.add_order(id_business=id_business,id_client=id_client,carts= carts,total_amount=total_amount)

            # print(response.get("id","no hay id"))
            
            return JsonResponse({"message": "Orden creada", "id_order": response,}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrderCanceledView(APIView):
    def post(self,request):
        try:
            data = json.loads(request.body)
            id_client= data.get("id_client","")
            id_order =data.get("idOrder","")
            id_business = data.get("id_business","")
            
            response = OrdersManager.remove_order(id_order)

            return JsonResponse({"response":response})
        except Exception as e: 
            return JsonResponse({"error": str(e)}, status= status.HTTP_400_BAD_REQUEST)


class OrderDashBoardView(APIView):
    def get(self,request):
        try:
            data = json.loads(request.body)
            
            idBusiness = data.get('idBusiness')
            orders = Order.objects.filter(id_business=idBusiness)
        
            analytics  = AnalyticsOrders(orders)
                
            return JsonResponse(analytics.reporte())
        except Exception as e :
            return JsonResponse({"error": str(e)}, status= status.HTTP_400_BAD_REQUEST)