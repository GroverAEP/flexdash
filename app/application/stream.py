# views.py
from django.http import StreamingHttpResponse
from django.utils.timezone import now
from .models import Order
import json
import time


class OrderStreamService:
    def __init__(self, order_repository):
        self.order_repository = order_repository

    def stream_orders(self):
        last_count = 0
        while True:
            orders = self.order_repository.get_all_orders()
            if len(orders) != last_count:
                last_count = len(orders)
                data = [
                    {"id": o.id, "status": o.status, "total_amount": float(o.total_amount)}
                    for o in orders
                ]
                yield f"data: {json.dumps(data)}\n\n"
            time.sleep(2)
            
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
