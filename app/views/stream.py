import json
import time
from django.http import StreamingHttpResponse
from app.models import Order
from app.content.orders import OrdersManager,AnalyticsOrders

def stream_orders(business_id):
    last_count = 0
    while True:
        # orders = Order.objects.filter(id_business=business_id)
        orders = OrdersManager.get_list_orders_id(idBusiness=business_id) # 
        if len(orders) != last_count:
            last_count = len(orders)
            # data = [
            #     {"id": str(o.id), "status": o.status, "total_amount": float(o.total_amount)}
            #     for o in orders
            # ]
            
            analyticsOrders = AnalyticsOrders(orders)
            # analyticsCustomers = A()
            
            
            order =  analyticsOrders.report_by_admin()
            # customer = 
            
            # data = {
            #     "order":order,
            #     "customers": c
            # }
            
            
            yield f"data: {json.dumps(order)}\n\n"
        time.sleep(2)

def orders_stream_view(request, business_id):
    response = StreamingHttpResponse(
        stream_orders(business_id),
        content_type='text/event-stream'
    )
    response['Cache-Control'] = 'no-cache'
    return response