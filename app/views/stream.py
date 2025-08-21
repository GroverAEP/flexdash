# application/views/order_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
from app.models import Order
import json
from app.content.orders import OrdersManager,AnalyticsOrders
from django.http import JsonResponse

from django.views import View

import json
import time
from django.http import StreamingHttpResponse,HttpResponseServerError
from app.models import Order
from app.content.orders import OrdersManager,AnalyticsOrders

from app.conexion import BDConnection ,ConexionOrderCache
from datetime import datetime, timedelta

import threading
class StreamOrder:
    # Atributo de clase (compartido entre todos)
    stream_queue_flag = False

    @classmethod
    def notify_stream(cls):
        cls.stream_queue_flag = True

    @classmethod
    def stream_orders(cls, business_id):
        # Conexión única al inicio
        collection = ConexionOrderCache.get_collection()
        analyticsOrders = AnalyticsOrders(idbusiness=business_id)

        # Snapshot inicial
        order = analyticsOrders.report_by_admin()
        yield f"data: {json.dumps(order)}\n\n"

        # Tiempo de última recarga completa
        last_refresh = datetime.now()

        # Pipeline de Change Stream
        pipeline = [
            {
                "$match": {
                    "operationType": {"$in": ["insert", "update", "replace"]},
                    "fullDocument.id_business": str(business_id)
                }
            }
        ]

        with collection.watch(pipeline=pipeline, full_document="updateLookup") as stream:
            for change in stream:
                print("📡 Cambio detectado en Mongo:", change)

                # --- 1) Actualización incremental ---
                if change["operationType"] == "insert":
                    analyticsOrders.lasted_orders.append(change["fullDocument"])

                elif change["operationType"] == "update":
                    for o in analyticsOrders.lasted_orders:
                        if o["id"] == change["documentKey"]["_id"]:
                            o.update(change["updateDescription"]["updatedFields"])
                            break

                elif change["operationType"] == "replace":
                    for i, o in enumerate(analyticsOrders.lasted_orders):
                        if o["id"] == change["documentKey"]["_id"]:
                            analyticsOrders.lasted_orders[i] = change["fullDocument"]

                # --- 2) Recalculo completo cada X tiempo ---
                if datetime.now() - last_refresh > timedelta(minutes=5):
                    print("♻️ Refrescando desde la BD...")
                    analyticsOrders = AnalyticsOrders(idbusiness=business_id)
                    last_refresh = datetime.now()

                # Enviar actualización
                order = analyticsOrders.report_by_admin()
                yield f"data: {json.dumps(order)}\n\n"
        

            # Pequeña pausa para no bloquear el CPU
    # @staticmethod
    # def stream_safe_pending_orders(business_id):
        # last_count = 0
        # while True:
        #     list_pending_orders = list(OrdersManager.get_list_orders_from_database(business_id))
        #     if len(list_pending_orders) != last_count:
        #         last_count = len(list_pending_orders)
        #         yield f"data: {json.dumps(list_pending_orders)}\n\n"
        #     time.sleep(2)  
    @staticmethod
    def stream_orders_today(business_id):
        last_count = 0
        while True:
            try:
                # 🔹 obtener lista de órdenes pendientes
                list_pending_orders = list(
                    OrdersManager.get_list_orders(idBusiness=business_id)
                )

                # 🔹 enviar solo si hay cambios
                if len(list_pending_orders) != last_count:
                    last_count = len(list_pending_orders)
                    payload = {
                        "today_orders": list_pending_orders
                    }
                    yield f"data: {json.dumps(payload)}\n\n"

            except Exception as e:
                # 🔹 loguear error en consola
                print("❌ Error en stream_orders_today:", str(e))

                # 🔹 enviar error al cliente SSE (opcional)
                error_msg = {"error": str(e)}
                yield f"data: {json.dumps(error_msg)}\n\n"

            # 🔹 pequeña pausa para no saturar CPU
            time.sleep(2)
    
    
    
    @staticmethod
    def stream_safe_pending_orders(business_id):
        pipeline = [
            {
                "$match": {
                    "fullDocument.id_business": business_id,
                    "fullDocument.status": "pending"
                }
            }
        ]

        try:
            collection, conexion = BDConnection.conexion_order_mongo()

            # 1️⃣ Emitir snapshot inicial (todas las órdenes pendientes actuales)
            try:
                initial_orders = list(OrdersManager.get_list_orders_pending_from_database(business_id))
                if initial_orders:
                    yield f"data: {json.dumps(initial_orders)}\n\n"
            except Exception as e:
                yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"

            # 2️⃣ Escuchar cambios en tiempo real
            with collection.watch(pipeline, full_document="updateLookup") as stream:
                for change in stream:
                    print("Modificación detectada en la colección:", change)

                    try:
                        # Vuelves a traer todas las órdenes pendientes
                        list_pending_orders = list(
                            OrdersManager.get_list_orders_pending_from_database(business_id)
                        )

                        yield f"data: {json.dumps(list_pending_orders)}\n\n"

                    except Exception as e:
                        yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"

        except Exception as e:
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
        finally:
            conexion.close()

    
    # @staticmethod
    # def stream_safe_completed_orders(business_id):
    #     pipeline = [
    #         {
    #             "$match": {
    #                 "fullDocument.id_business": business_id,
    #                 "fullDocument.status": "completed"
    #             }
    #         }
    #     ]

    #     try:
    #         collection, conexion = BDConnection.conexion_order_mongo()

    #         # 1️⃣ Emitir snapshot inicial (todas las órdenes pendientes actuales)
    #         try:
    #             initial_orders = list(OrdersManager.get_list_orders_pending_from_database(business_id))
    #             if initial_orders:
    #                 yield f"data: {json.dumps(initial_orders)}\n\n"
    #         except Exception as e:
    #             yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"

    #         # 2️⃣ Escuchar cambios en tiempo real
    #         with collection.watch(pipeline, full_document="updateLookup") as stream:
    #             for change in stream:
    #                 print("Modificación detectada en la colección:", change)

    #                 try:
    #                     # Vuelves a traer todas las órdenes pendientes
    #                     list_pending_orders = list(
    #                         OrdersManager.get_list_orders_pending_from_database(business_id)
    #                     )

    #                     yield f"data: {json.dumps(list_pending_orders)}\n\n"

    #                 except Exception as e:
    #                     yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"

    #     except Exception as e:
    #         yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
    #     finally:
    #         conexion.close()

    


class OrdersStreamTodayView(View):
    def get(self,request,business_id):
        try:
            response = StreamingHttpResponse(
                StreamOrder.stream_orders_today(business_id=business_id),
                content_type='text/event-stream'

            )
            response['Cache-Control'] = 'no-cache'
            response['X-Accel-Buffering'] = 'no'
            return response

        except Exception as e:
                # ⚠️ Si algo falla antes de empezar el stream, devolvemos un error normal
                print(f"Error en OrdersStreamSafeView: {e}")
                return HttpResponseServerError("Error iniciando el stream")



class OrdersStreamView(View):
    def get(self, request, business_id):
        response = StreamingHttpResponse(
            StreamOrder.stream_orders(business_id),
            content_type='text/event-stream'
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response


class OrdersStreamSafeView(View):
    def get(self, request, business_id):
        try:
            response = StreamingHttpResponse(
                StreamOrder.stream_safe_pending_orders(business_id),
                content_type='text/event-stream'
            )
            response['Cache-Control'] = 'no-cache'
            response['X-Accel-Buffering'] = 'no'
            return response

        except Exception as e:
            # ⚠️ Si algo falla antes de empezar el stream, devolvemos un error normal
            print(f"Error en OrdersStreamSafeView: {e}")
            return HttpResponseServerError("Error iniciando el stream")
