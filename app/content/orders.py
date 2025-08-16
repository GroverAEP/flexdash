from datetime import datetime, timedelta

from threading import Lock
from statistics import mean
from app.models import Order
from django.utils import timezone
import uuid 

from app.conexion import BDConnection
from app.serializers import OrderSerializer
from app.content.client import ClientManager
from decimal import Decimal


class OrdersManager:
    orders= {}
    lock = Lock()
    
    def __init__(self):
        self.orders = {}  # key = order_id, value = dict con datos de la orden
        self.lock = Lock()

    @classmethod
    def upload_orders(cls):
        try:    
            print("ejecutando_order_db")
            list_orders = cls.get_list_orders_date()
            
            collection, conexion = BDConnection.conexion_order_mongo()

            collection.insert_many(list_orders)
            conexion.close()
            
            cls.remove_orders_date()
        except Exception as e:
            print(e)

    @staticmethod
    def remove_orders_date():
                # Fecha actual (solo día, mes, año)
        hoy = datetime.now() 
        # print(hoy)
        # dos_dias_Despues = datetime.now() - timedelta(days=1)
        # print(dos_dias_Despues)
        
        # Filtrar y eliminar órdenes cuya fecha de creación sea menor a hoy
        resp = Order.objects.filter(date__lt=hoy).delete()
        print(resp)    


    @classmethod
    def add_order(cls, id_business,id_client, carts, total_amount, status="pending"):
        """Crea una nueva orden en DB y la guarda en memoria"""
        with cls.lock:
            
            
            
            
            #proceso agregar por objeto
            order = Order.objects.create(
                id_business= uuid.UUID(id_business) if id_business else uuid.uuid4(),
                id_client= uuid.UUID(id_client) if id_client else uuid.uuid4(),
                carts=carts,
                total_amount=total_amount,
                status=status,
                date=timezone.now() - timedelta(days=2)
            )
                
                
            adminUserSerializer = OrderSerializer(order)
            json_order = adminUserSerializer.data  
           
            print(json_order)
            cls.orders[str(order.id)] = {
                "obj": order,  # instancia real del modelo
                "created_at": str(datetime.now()),
                "updated_at": None,
                "historial": [("creada", datetime.now())]
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
        print(self.orders)
        
        result = Order.objects.filter(id=order_id).delete()
        
        if result :
            return {
                    "message": "Orden Eliminada",
                    "status": True,
                    "id": order_id,
                    # "self": self.orders
                }
        
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
    def get_list_orders_id(cls, idBusiness: str):
        list_orders = Order.objects.filter(id_business=idBusiness)
        orderSerializer = OrderSerializer(list_orders, many=True)
        return orderSerializer.data
    
    @classmethod
    def get_list_orders_date():
        hoy = datetime.now()
        list_orders = Order.objects.filter(date__lt=hoy)
        
        orderSerializer= OrderSerializer(list_orders,many=True)
        json_data = orderSerializer.data
        
        return json_data


    @classmethod
    def get_list_orders(self):

        list_orders = Order.objects.all()
        
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
        y filtra solo las órdenes del negocio indicado.
        """
        print("analitic orders")
        # print(id_business)
        print(orders_queryset)
        # Convertimos a UUID si llega como string
        # if isinstance(id_business, str):
        #     id_business = uuid.UUID(id_business)
        # self = Order.objects.filter(id_business= id_business)
        
        for order in orders_queryset:
            print(order)
            response = ClientManager(id_client=str(order["id_client"])).get_client_id()  
            order["client"] = response

        self.orders = orders_queryset 
        
        # [o for o in orders_queryset if o.id_business == id_business]
        print("ejecuctando sel.orders")
        
        print(self.orders)
        
    # Conteo de órdenes por estados
    @property
    def quantity_pending(self):
        return sum(1 for o in self.orders if o["status"] == "pending")

    @property
    def quantity_completed(self):
        return sum(1 for o in self.orders if o["status"] == "completed")
    
    @property
    def quantity_cancelled(self):
        return sum(1 for o in self.orders if o["status"] == "cancelled")

    # Listas de órdenes por estado
    @property
    def pending_orders(self):
        return [o for o in self.orders if o["status"] == "pending"]

    @property
    def completed_orders(self):
        return [o for o in self.orders if o["status"] == "completed"]

    @property
    def cancelled_orders(self):
        return [o for o in self.orders if o["status"] == "cancelled"]

    # Ganancia de órdenes completadas
    @property
    def earn_today(self):
        return sum(Decimal(o["total_amount"]) for o in self.completed_orders)

    # Tiempo promedio de procesado (si aplica)
    @property
    def tiempo_promedio_procesado(self):
        from statistics import mean
        tiempos = [
            (o.updated_at - o.created_at).total_seconds()
            for o in self.orders
            if o.status == "finalizada" and o.updated_at
        ]
        return mean(tiempos) if tiempos else 0

    # Reporte para admin
    def report_by_admin(self):
        return {    
            "total": self.orders,
            "pending": self.pending_orders,
            "completed": self.completed_orders,
            "cancelled": self.cancelled_orders,
            "earn_today": str(self.earn_today),
            # "tiempo_promedio_procesado_seg": self.tiempo_promedio_procesado
        }

    # Reporte para cliente
    def report_by_client(self, id_client):
        orders_client = [o for o in self.orders if o.id_client == id_client]
        return {
            "total": len(orders_client),
            "orders": orders_client
        }
        

    