from app.content.orders import OrdersManager
from django.http import JsonResponse

def upload_orders_view(request):
    OrdersManager.upload_orders()
    return JsonResponse({"status": "ok"})