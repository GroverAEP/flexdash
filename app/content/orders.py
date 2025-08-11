import datetime

from threading import Lock
from statistics import mean
from app.models import Order
from django.utils import timezone
import datetime
import uuid 

from app.serializers import OrderSerializer

class OrdersManager:
    orders= {}
    lock = Lock()
    
    def __init__(self):
        self.orders = {}  # key = order_id, value = dict con datos de la orden
        self.lock = Lock()

    @classmethod
    def add_order(cls, id_business,id_client, carts, total_amount, status="pending"):
        """Crea una nueva orden en DB y la guarda en memoria"""
        with cls.lock:
            order = Order.objects.create(
                id_business= uuid.UUID(id_business) if id_business else uuid.uuid4(),
                id_client= uuid.UUID(id_client) if id_client else uuid.uuid4(),
                carts=carts,
                total_amount=total_amount,
                status=status,
                date=timezone.now()
            )
                
                
            adminUserSerializer = OrderSerializer(order)
            json_order = adminUserSerializer.data  
           
            print(json_order)
            cls.orders[str(order.id)] = {
                "obj": order,  # instancia real del modelo
                "created_at": str(datetime.datetime.now()),
                "updated_at": None,
                "historial": [("creada", datetime.datetime.now())]
            }
            
            

            return json_order["id"]

    
    def update_order(self, order_id, **kwargs):
        """Actualiza datos de una orden existente (memoria + DB)"""
        with self.lock:
            if order_id in self.orders:
                order_info = self.orders[order_id]

                # Actualiza en DB
                order = order_info["obj"]
                for field, value in kwargs.items():
                    setattr(order, field, value)
                order.save()

                # Actualiza en memoria
                order_info["updated_at"] = datetime.datetime.now()
                order_info["historial"].append(
                    (f"actualizada → {kwargs}", datetime.datetime.now())
                )
    
    
    @classmethod
    def remove_order(self, order_id):
        """Elimina la orden de memoria y DB"""
        with self.lock:
            if order_id in self.orders:
                order_obj = self.orders[order_id]["obj"]  # instancia real
                order_obj.delete()
                del self.orders[order_id]
                return {
                    "message": "Orden Eliminada",
                    "status": True,
                    "id": order_id,
                    "self": self.orders
                }
            return {
                "message": "Orden no existe",
                "status": False,
                "id": order_id
            }
    
    @classmethod
    def get_list_orders(self,idBusiness):
        list_orders = Order.objects.filter(id_business = idBusiness)
        
        orderSerializer= OrderSerializer(list_orders,many=True)
        json_data = orderSerializer.data
        
        return json_data



#AnALISIS PARA SOLAMENTE MEMORIA 

# class AnalyticsOrders:
#     def __init__(self, orders_manager):
#         self.orders_manager = orders_manager

#     @property
#     def cantidad_pendientes(self):
#         return sum(1 for o in self.orders_manager.orders.values() if o["status"] == "pending")

#     @property
#     def cantidad_pagadas(self):
#         return sum(1 for o in self.orders_manager.orders.values() if o["status"] == "pagada")

#     @property
#     def cantidad_finalizadas(self):
#         return sum(1 for o in self.orders_manager.orders.values() if o["status"] == "finalizada")

#     @property
#     def tiempo_promedio_procesado(self):
#         tiempos = []
#         for o in self.orders_manager.orders.values():
#             if o["status"] == "finalizada" and o["updated_at"]:
#                 diff = (o["updated_at"] - o["created_at"]).total_seconds()
#                 tiempos.append(diff)
#         return mean(tiempos) if tiempos else 0

#     def search_for_cliente(self, id_client):
#         return {
#             oid: o for oid, o in self.orders_manager.orders.items()
#             if o.get("id_client") == id_client
#         }

#     def search_for_estado(self, estado):
#         return {oid: o for oid, o in self.orders_manager.orders.items() if o["status"] == estado}

#     def search_for_negocio(self, id_business):
#         return {
#             oid: o for oid, o in self.orders_manager.orders.items()
#             if o.get("id_business") == id_business
#         }

#     def reporte(self):        
#         return {
#             "total": len(self.orders_manager.orders),
#             "pendientes": self.cantidad_pendientes,
#             "pagadas": self.cantidad_pagadas,
#             "finalizadas": self.cantidad_finalizadas,
#             "tiempo_promedio_procesado_seg": self.tiempo_promedio_procesado
#         }


#     def reporte_for_business(self, id_business=None):
#         if id_business:
#             orders = {
#                 oid: o for oid, o in self.orders_manager.orders.items()
#                 if o["obj"].id_business == id_business
#             }
#         else:
#             orders = self.orders_manager.orders

#         return {
#             "total": len(orders),
#             "pendientes": sum(1 for o in orders.values() if o["obj"].status == "pending"),
#             "pagadas": sum(1 for o in orders.values() if o["obj"].status == "pagada"),
#             "finalizadas": sum(1 for o in orders.values() if o["obj"].status == "finalizada"),
#             "tiempo_promedio_procesado_seg": self._tiempo_promedio(orders)
#         }



class AnalyticsOrders:
    def __init__(self, orders_queryset):
        """
        Recibe un QuerySet o lista de órdenes (instancias del modelo Order)
        """
        self.orders = list(orders_queryset)  # Lo convertimos a lista para reusar fácilmente

    @property
    def quantity_pending(self):
        return sum(1 for o in self.orders if o.status == "pending")

    @property
    def quantity_completed(self):
        return sum(1 for o in self.orders if o.status == "completed")
    
    @property
    def quantity_cancelled(self):
        return sum(1 for o in self.orders if o.status == "cancelled")

    # @property
    # def cantidad_finalizadas(self):
    #     return sum(1 for o in self.orders if o.status == "finalizada")

    @property
    def tiempo_promedio_procesado(self):
        tiempos = []
        for o in self.orders:
            if o.status == "finalizada" and o.updated_at:
                diff = (o.updated_at - o.created_at).total_seconds()
                tiempos.append(diff)
        return mean(tiempos) if tiempos else 0

    def search_for_cliente(self, id_client):
        return [o for o in self.orders if o.id_client == id_client]

    def search_for_estado(self, estado):
        return [o for o in self.orders if o.status == estado]

    def search_for_negocio(self, id_business):
        return [o for o in self.orders if o.id_business == id_business]

    def reporte(self):
        return {
            "total": len(self.orders),
            "pending": self.quantity_pending,
            "complete": self.quantity_completed,
            "cancelled": self.quantity_cancelled,
            "tiempo_promedio_procesado_seg": self.tiempo_promedio_procesado
        }