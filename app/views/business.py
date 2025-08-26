from app.content.business import BusinessManager

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
from app.models import Order
import json
from app.content.orders import OrdersManager,AnalyticsOrders
from django.http import JsonResponse



class BusinessGetIdInfoView(APIView):
    def post(self,request):
            try:
                data = json.loads(request.body)
                id_business = data.get("idBusiness")
                response = BusinessManager.get_business_id(id_business=id_business)
                return JsonResponse({"respose":response})
            except Exception as e:
                return JsonResponse({"error":str(e)},status=400)   