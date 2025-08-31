from app.content.business import BusinessManager

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import uuid
from app.models import Order
import json
from app.content.orders import OrdersManager,AnalyticsOrders
from django.http import JsonResponse



class BusinessGetIdInfoView(APIView):
    permission_classes = []  # 👈 así se hace en clase
    # authentication_classes = [] 
    authentication_classes = []
    def post(self,request):
            try:
                data = json.loads(request.body)
                id_business= data.get("idBusiness")
                print(id_business)
                response = BusinessManager.get_business_id(id_business=id_business)
                print(response)
                return JsonResponse(
                    {"response": response
                    
                     
                     })
            except Exception as e:
                return JsonResponse({"error":str(e)},status=400)    