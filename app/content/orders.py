from datetime import datetime, timedelta

from threading import Lock
from statistics import mean
from app.models import Order
from django.utils import timezone
import uuid 

from app.conexion import BDConnection , ConexionOrderCache
from app.serializers import OrderSerializer
from app.content.client import ClientManager
from decimal import Decimal
from uuid import UUID


class OrdersManager:
    orders= {}
    lock = Lock()
    
    def __init__(self):
        self.orders = {}  # key = order_id, value = dict con datos de la orden
        self.lock = Lock()

    @classmethod
    def get_list_orders_id_client_id_business(cls,id_client:str,id_business:str):
        try:
            list_orders_client = []

            print(id_client)

            # Obteniendo ordenes de la nube (MongoDB):
            collection, conexion  = BDConnection.conexion_order_mongo()
            list_orders_bd =  list(collection.find(
                                    {"id_client": id_client,
                                     "id_business": id_business,
                                     "status":"pending"
                                     },
                                    
                                    {"_id": 0}))

            print(list_orders_bd)
            
            # Obteniendo ordenes de los objetos (Django ORM):
            list_orders_objects = list(Order.objects.filter(
                    id_client=uuid.UUID(id_client),
                    status = "pending",
                    id_business=uuid.UUID(id_business)).values())
            print(list_orders_objects)

            # Uniendo todas las ordenes:
            list_orders_client = list_orders_bd + list_orders_objects
                        
            conexion.close()
            return list_orders_client
        except Exception as e :
            return {
                "status":400,
                "error": str(e)}

    @classmethod
    def cancelled_order_process(cls,id_order:str,data:dict,reason:str):
        try:   
            #primero identificamos si la orden es pasada o de hoy
            update_data = {
                    "status":"cancelled",
                    "carts.reason": reason,
                    "update_data": timezone.now().isoformat()
            }
            
            print("COMPROVANDO VALIDATEORDER")
            print(Order.objects.filter(id=UUID(id_order)).exists())
            print(Order.objects.filter(id=id_order).exists())
            
            if Order.objects.filter(id=UUID(id_order)).exists():
                data["status"] = "cancelled"
                data["update_date"] = timezone.now().isoformat()
                data["carts"]["reason"]  =reason
                
                cls.upload_order_completed(id_order=id_order,upload_data=data)
                
                Order.objects.filter(id=id_order).delete()
            else:
                cls.update_order_status(id_order=id_order,update_data=update_data)
                
        
        except Exception as e:
            print("🔥 Error en PaymentProcess:", e) 
        



    @classmethod
    def validated_order_process(cls,id_order:str,data:dict):
        try:
            #primero identificamos si la orden es pasada o de hoy
            update_data = {
                    "status":"completed",
                    "update_data": timezone.now().isoformat()
            }
            
            print("COMPROVANDO VALIDATEORDER")
            print(Order.objects.filter(id=UUID(id_order)).exists())
            print(Order.objects.filter(id=id_order).exists())
            
            if Order.objects.filter(id=UUID(id_order)).exists():
                data["status"] = "completed"
                data["update_date"] = timezone.now().isoformat()
                
                
                cls.upload_order_completed(id_order=id_order,upload_data=data)
                
                Order.objects.filter(id=id_order).delete()
            else:
                cls.update_order_status(id_order=id_order,update_data=update_data)
                
        
        except Exception as e:
            print("🔥 Error en PaymentProcess:", e)            

    @classmethod
    def upload_order_completed(cls,id_order, upload_data):
        
        try:
            collection, conexion = BDConnection.conexion_order_mongo()

            # 🔹 Actualizamos la orden por su id
            result = collection.insert_one(upload_data)
                # {"id": str(id_order)},      # filtro por id
                # {"$set": update_data}       # campos a actualizar
            
            if result.inserted_id:
                print(f"✅ Orden {id_order} insertada correctamente en Mongo con _id {result.inserted_id}")
            else:
                print(f"⚠️ No se pudo insertar la orden {id_order}")

            conexion.close()

            # Opcional: eliminar la orden de algún lugar temporal si aplica
            # cls.remove_order(order_id=order_id)

        except Exception as e:
            print("🔥 Error en PaymentProcess:", e)
            
    @classmethod
    def update_order_status(cls, id_order, update_data):
        """
        Recibe un `order_id` y un dict `update_data` con los campos a actualizar.
        """
        try:
            collection, conexion = BDConnection.conexion_order_mongo()

            # 🔹 Actualizamos la orden por su id
            result = collection.update_one(
                {"id": str(id_order)},      # filtro por id
                {"$set": update_data}       # campos a actualizar
            )

            if result.matched_count:
                print(f"✅ Orden {id_order} actualizada correctamente")
            else:
                print(f"⚠️ No se encontró la orden {id_order} para actualizar")

            conexion.close()

            # Opcional: eliminar la orden de algún lugar temporal si aplica
            # cls.remove_order(order_id=order_id)

        except Exception as e:
            print("🔥 Error en  paymentStatus oder:", e)














    @classmethod
    def upload_orders(cls):
        try:    
            print("ejecutando_order_db")
            list_orders = cls.get_list_orders_date()
            
            collection, conexion = BDConnection.conexion_order_mongo()
            if list_orders:
                collection.insert_many(list_orders)
            else:
                print("⚠️ No hay órdenes para subir a Mongo")
            # collection.insert_many(list_orders)
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
    def add_order(cls, id_business,id_client, carts, total_amount,data,status="pending",):
        """Crea una nueva orden en DB y la guarda en memoria"""
        with cls.lock:
            
            
            
            
            #proceso agregar por objeto
            order = Order.objects.create(
                id_business= uuid.UUID(id_business) if id_business else uuid.uuid4(),
                id_client= uuid.UUID(id_client) if id_client else uuid.uuid4(),
                data = data,
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

        # Eliminar de MongoDB
        collection, conexion = BDConnection.conexion_order_mongo()
        result_order_bd = collection.delete_one({"id": order_id,"status":"pending"})
        deleted_mongo = result_order_bd.deleted_count > 0
        conexion.close()

        # Eliminar de Django ORM
        deleted_sql_count, _ = Order.objects.filter(id=order_id,status="pending").delete()
        deleted_sql = deleted_sql_count > 0

        if deleted_mongo or deleted_sql:
            return {
                "message": "Orden Eliminada",
                "status": True,
                "id": order_id,
            }

        return {
            "message": "Orden no existe",
            "status": False,
            "id": order_id
        }
        # with self.lock:
        #     if order_id in self.orders:
        #         order_obj = self.orders[order_id]["obj"]  # instancia real
        #         order_obj.delete()
        #         del self.orders[order_id]
        #         return {
        #             "message": "Orden Eliminada",
        #             "status": True,
        #             "id": order_id,
        #             "self": self.orders
        #         }
    
    @classmethod
    def get_list_orders_id(cls, idBusiness: str):
        collection, conexion = BDConnection.conexion_order_mongo()
        today = timezone.now()
                # Rango: desde el inicio de hoy hasta el inicio de mañana
        start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        
        list_order_completed = list(collection.find({
            # "status": "completed",
            "date": {"$gte": start.isoformat(), "$lt": end.isoformat()}
        }, {"_id": 0}))

        list_orders = Order.objects.filter(id_business=idBusiness)
        orderSerializer = OrderSerializer(list_orders, many=True)

        # Unir ambas listas
        combined = list_order_completed + orderSerializer.data

        conexion.close()
        return combined
    
    
    
    
    #metodo para obtener la lista de ordenes que estan guardadas en la basede datos
    @classmethod

    def get_list_orders_from_database(cls, idBusiness: str, status: str = None):
        #llamao conexion bdOrder
        collection= ConexionOrderCache.get_collection()
        
        if status:
            list_orders = list(
                collection.find(
                    {"id_business": str(idBusiness), "status": status},
                    {"_id": 0}
                )
            )
        else:
            list_orders = list(
                collection.find(
                    {"id_business": str(idBusiness)},
                    {"_id": 0}
                    
                )
            )
        
        
        print("ordenManager,bd")
        print(list_orders)
        
        #cierro conexion
        # conexion.close()
        return list_orders
    
    
    # @classmethod
    # # def get_earn_month():
    # #         cl
    # #     return
    
    
    
    
    @classmethod
    def get_list_orders_pending_from_database(cls,idBusiness:str):
        return cls.get_list_orders_from_database(idBusiness=idBusiness, status="pending")
    
    @classmethod
    def get_list_orders_completed_from_database(cls,idBusiness:str):
        return cls.get_list_orders_from_database(idBusiness=idBusiness, status="completed")
    
    @classmethod
    def get_list_orders_cancelled_from_database(cls,idBusiness:str):
        return cls.get_list_orders_from_database(idBusiness=idBusiness, status="cancelled")
    
    @classmethod
    def get_list_orders_total_from_database(cls,idBusiness:str):
        return cls.get_list_orders_from_database(idBusiness=idBusiness)
        
    
    
    @classmethod
    def get_list_orders_date(cls,idBusiness:str):
        hoy = timezone.now()  # ✅ aware datetime
        list_orders = Order.objects.filter(id_business=idBusiness,date__lt=hoy)
        print("lista de ordenes")
        print()
        orderSerializer= OrderSerializer(list_orders,many=True)
        json_data = orderSerializer.data
        
        return json_data


    @classmethod
    def get_list_orders(self,idBusiness):

        list_orders = Order.objects.filter(id_business=idBusiness)
        
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
    def __init__(self,idbusiness):
        
        try:
            self.lasted_orders = OrdersManager.get_list_orders_total_from_database(idBusiness=idbusiness)
            self.today_orders = OrdersManager.get_list_orders_date(idBusiness=idbusiness)
            print("ejecutando analitic orders")
        except Exception as e:
            print(f"🔥 Error en AnalyticsOrders.__init__: {e}")
            # opcional: puedes asignar listas vacías para que el objeto siga existiendo
            self.lasted_orders = []
            self.today_orders = []

    # Conteo de órdenes por estados
    @property
    def quantity_pending(self):
        return sum(1 for o in self.lasted_orders if o["status"] == "pending")

    @property
    def quantity_completed(self):
        return sum(1 for o in self.lasted_orders if o["status"] == "completed")
    
    @property
    def quantity_cancelled(self):
        return sum(1 for o in self.lasted_orders if o["status"] == "cancelled")

    # Listas de órdenes por estado
    @property
    def pending_orders(self):
        return [o for o in self.lasted_orders if o["status"] == "pending"]


    @property
    def pending_lasted(self):
        pass

    @property
    def pending_orders(self):
        return [o for o in self.lasted_orders if o["status"] == "pending"]

    @property
    def completed_orders(self):
        return [o for o in self.lasted_orders if o["status"] == "completed"]

    @property
    def cancelled_orders(self):
        return [o for o in self.lasted_orders if o["status"] == "cancelled"]

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

    

    def report_earn_month(self):
        try:
            list_month=[f"{i:02}" for i in range(1,13)]
            
            # print(list_month)
            # list_earn_month = [
            #     {"id": "1AKOSOk2oad", "total_amount": 32, "update_date": "2025-08-20T00:51:01.659105+00:00"},
            #     {"id": "2AKOSOk2oad", "total_amount": 20, "update_date": "2025-08-19T05:06:09.364504+00:00"},
            #     {"id": "3AKOSOk2oad", "total_amount": 20, "update_date": "2025-07-20T02:52:28.650380+00:00"},
            #     {"id": "5AKOSOk2oad", "total_amount": 32, "update_date": "2025-06-20T04:16:05.647452+00:00"},
            # ]
            # 🔹 1. Convertimos fechas y las agrupamos por mes
                # 🔹 1. Inicializamos con 0 en todos los meses
            suma_por_mes = {m: 0 for m in list_month}
            
            
            
            # 🔹 2. Recorremos las órdenes y sumamos por mes
            for o in self.completed_orders:
                dt = datetime.fromisoformat(o["update_date"].replace("Z", "+00:00"))
                mes = f"{dt.month:02}"  # "06", "07", "08"
                suma_por_mes[mes] += Decimal( o["total_amount"])
            # 🔹 Convertir Decimals a float para JSON
                resultado = [float(suma_por_mes[f"{m:02}"]) for m in range(1,13)]

            # 🔹 3. Resultado
            print("suma")
            print(resultado)
            return resultado
        except Exception as e:
            "error"
            print(e)
        
    # Reporte para admin
    def report_by_admin(self):
        #         # --- set de IDs de órdenes pendientes en el histórico ---
        # pending_ids = {o["id"] for o in self.lasted_orders if o["status"] == "pending"}

        # # --- cuáles de esos pasaron a completed hoy ---
        # completed_today_from_pending = [
        #     o for o in self.today_orders
        #     if o["status"] == "completed" and o["id"] in pending_ids
        # ]

        
        
        return {
            "total_orders": len(self.lasted_orders),
            "today_orders": self.today_orders,
            "pending": self.pending_orders,
            "cancelled": self.cancelled_orders,
            "completed": self.completed_orders,
            # "last_orders"
            "orders": {
                "all": self.lasted_orders,
                "today": self.today_orders
            },
            "status_summary": {
                "total": len(self.lasted_orders) + len(self.today_orders),
                "today": len(self.today_orders),
                "pending": len([o for o in self.lasted_orders if o["status"] == "pending"]),
                "completed": len([o for o in self.lasted_orders if o["status"] == "completed"]),
                "cancelled": len([o for o in self.lasted_orders if o["status"] == "cancelled"]),
            },
            "earn_today": str(self.earn_today),
            # "completed_today_from_pending": completed_today_from_pending
        }

    # Reporte para cliente
    def report_by_client(self, id_client):
        orders_client = [o for o in self.orders if o.id_client == id_client]
        return {
            "total": len(orders_client),
            "orders": orders_client
        }
        

    