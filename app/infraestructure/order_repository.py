from orders.domain.order_repository import OrderRepository
from orders.models import Order

class OrderRepositoryDjango(OrderRepository):
    def get_all_orders(self):
        return Order.objects.all()