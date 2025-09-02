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
    permission_classes = []  # 👈 así se hace en clase
    authentication_classes = []
    def post(self, request):
        try:
            info = json.loads(request.body)
            # uuid.UUID(data.get("idBusiness")) if data.get("idBusiness") else uuid.uuid4()
            # uuid.UUID(data.get("idClient")) if data.get("idClient") else uuid.uuid4()
            id_business = info.get("idBusiness") if info.get("idBusiness") else uuid.uuid4()
            id_client = info.get("idClient") if info.get("idClient") else uuid.uuid4()
            total_amount=info.get("total_amount")
            carts= info.get("carts", {})
            data_cl = info.get("data",{})
            
            print(data_cl)
            response = OrdersManager.add_order(
                    id_business=id_business,
                    id_client=id_client,
                    carts=carts,
                    total_amount=total_amount
                    ,data=data_cl)

            # print(response.get("id","no hay id"))
            
            return JsonResponse({"message": "Orden creada", "id_order": response,}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrderCanceledView(APIView):
    permission_classes = []  # 👈 así se hace en clase
    authentication_classes = []
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

class OrderGetIdClientView(APIView):
    permission_classes = []  # 👈 así se hace en clase
    authentication_classes = []
    def post(self,request):
        try:
            data = json.loads(request.body)
            idClient = data.get("idClient")
            idBusiness = data.get("idBusiness")
            print(idClient)
            
            response = OrdersManager.get_list_orders_id_client_id_business(
                id_client=str(idClient),
                id_business=idBusiness)
            return JsonResponse({"response":response})
            # return JsonResponse({"a":"listo"})
        except Exception as e:
            return JsonResponse({"error":str(e)},status=400)   
            
class OrderGetList(APIView):
    def post(self,request):
        try:
             # Opción 1: Si el ID viene en el JSON del body
            data = request.data  # DRF ya parsea el JSON automáticamente
            id_business = data.get("id")
            
            # Opción 2: Si prefieres leer el body manualmente (no recomendado con DRF)
            # raw_data = json.loads(request.body)
            # id_business = raw_data.get("id")

            if not id_business:
                return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            response = OrdersManager.get_list_orders(idBusiness=id_business)

            return JsonResponse(response,safe=False)
        except Exception as e:
            return JsonResponse({ "error": str(e)})


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