from app.models import ClientUser,FollowBusiness,Cart,CartPayment,Products
from app.models import AdminUser, Business,TimeZone,MethodPayment,SocialMedia,Feedback,CoWorker,Catalog,CatalogImage,CatalogItem

from app.conexion import BDConnection
from datetime import datetime
from .serializers import  ClientUserSerializer,AdminUserSerializer,CatalogSerializer
import json
from django.http import HttpResponse , JsonResponse

from decimal import Decimal
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from zoneinfo import ZoneInfo
import urllib.parse


import mercadopago
import os
import requests
import uuid

class AdminContent():
    @classmethod
    def add_user(self, serializable:json):
        collection ,conexion= BDConnection.conexion_admin_mongo()
        
        print("Campo-SEriizable")
        print(serializable)
        print("Campo-SEriizable")
        
        #creacion modelo 
        # Datos del Admin
        user = AdminUser.objects.create(
            full_name=serializable["full_name"],
            first_name=serializable["first_name"],
            last_name=serializable["last_name"],
            dni=serializable["dni"],
            phone=serializable["phone"],
            country=serializable["country"],
            email=serializable["email"],
        )
        
        print(user.full_name)
        
        print(serializable["business"])
        
        if "business" in serializable:
            for b in serializable.get("business"):
                print("business")
                
                business = Business.objects.create(
                    AdminUser=user,
                    idBot=b['idBot'],
                    name=b['name'],
                    category=b['category'],
                    ruc=b['ruc'],
                    phone_number=b['phone_number'],
                    phone_country_code=b['phone_country_code'],
                    catalog_url=b['catalog_url'],
                    description=b['description'],
                    address=b['address'],
                    logo_url=b['logo_url']
                )

                print(business)  # ✅ Ahora sí existe

                if "catalog" in b:
                    bc = b["catalog"]
                    catalog = Catalog.objects.create(
                        business=business,
                    )
                    print(catalog)

                    # Creamos imágenes
                    if "catalog_images" in bc:
                        for catalog_image in bc["catalog_images"]:
                         catalog_image_object= CatalogImage.objects.create(
                                catalog=catalog,
                                name=catalog_image["name"],
                                type=catalog_image["type"],
                                img_url=catalog_image["img_url"]
                            )
                    # Creamos items
                    if "catalog_items" in bc:
                        for catalog_item in bc["catalog_items"]:
                            print(catalog_item)
                            print(catalog_item["price"])
                            CatalogItem.objects.create(
                                catalog=catalog,
                                name=catalog_item["name"],
                                description=catalog_item.get("description", ""),
                                type=catalog_item["type"],
                                price=catalog_item["price"],
                                stock=catalog_item["stock"]
                            )

                    # ✅ Serializamos el catálogo recién creado (con imágenes e items ya guardados)
                    catalog_serializer = CatalogSerializer(catalog)
                    b["catalog"] = catalog_serializer.data


                if "method_payment" in b:
                    mp = b["method_payment"]
                    MethodPayment.objects.create(
                            business=business,
                            type=mp["type"],
                            name=mp["name"],
                            lastName=mp.get("lastName", ""),
                            email=mp.get("email", ""),
                            phone=mp.get("phone", ""),
                            phone_number=mp.get("phone_number", ""),
                            country_code=mp.get("country_code", ""),
                            qrImageUrl=mp.get("qrImageUrl", ""),
                            account_token=mp.get("account_token", ""),
                            public_key=mp.get("public_key", "")
                        )
                
                    print("social_media")

                if "social_media" in b:
                    for sm in b["social_media"]:
                        print(sm)
                        SocialMedia.objects.create(
                            business=business,
                            type_social=sm["type_social"],
                            urlPage=sm["urlPage"]
                        )

                if "co_workers" in b:
                    for cw in b["co_workers"]:
                        # cw = serializable["co_workers"] 
                        CoWorker.objects.create(
                            business=business,
                            coworker_id=cw.get("coworker_id", ""),
                            status=cw.get("status", "")
                        )

                if "feedback" in b:
                    
                    for  fb in b["feedback"]:
                    
                        Feedback.objects.create(
                            business=business,
                            name=fb["name"],
                            message=fb.get("message", "")
                        )

                if "time_zone" in b:
                        tz = b["time_zone"]
                        TimeZone.objects.create(
                            business = business,
                                time_open = tz["time_open"],
                                time_close = tz["time_close"]
                        )
            
        adminUserSerializer = AdminUserSerializer(user)
        json_data = adminUserSerializer.data

        print("parte final")
        print(json_data)

        collection.insert_one(json_data)
        

        conexion.close()
    @classmethod
    def search_id_catalog(cls, id):
        collection, conexion = BDConnection.conexion_admin_mongo()

        try:
            # Buscar documento con ese ID
            doc = collection.find_one({"id": id})

            if not doc:
                return JsonResponse({
                    "status": 404,
                    "message": "Documento no encontrado"
                })

            # Asegurar que 'catalog' y 'catalog_items' existan
            catalog = doc.get("business", [])[0].get("catalog") if doc.get("business") else None
            catalog_items = catalog.get("catalog_items") if catalog else None

            print("catalog - Business")
            print(catalog_items)
            
            return catalog_items
            

            # return JsonResponse({
            #     "status": 200,
            #     "data": catalog_items or []
            # })


        except Exception as e:
            conexion.close()
            return JsonResponse({
                "status": 500,
                "error": str(e)
            })

class ClientContent():
    @classmethod
    def add_user(self,serializable:json):
        collection, conexion = BDConnection.conexion_client_mongo()
        
        #creacion del modelo
        user = ClientUser.objects.create(
            # id = serializable["idClient"],
            full_name= serializable["full_name"],
            first_name = serializable["first_name"],
            last_name = serializable["last_name"],
            country = serializable["country"],
            email = serializable["email"],
            phone = serializable["phone"],
        )

        follow_business_list = []
        if "follow_business" in serializable and serializable["follow_business"]:
            for fb in serializable["follow_business"]:
               
                follow_business = FollowBusiness.objects.create(
                    clientUser=user,
                    id_conversation=fb["id_conversation"],
                    type=fb["type"]
                )
                
                print(follow_business)
                print(fb)
                print(fb.get("cart_payment"))
                
                if "cart_payment" in fb:
                    # print("true")
                    print()
                    print(fb.get("cart_payment")['cart_status'])
                    cartp = fb.get("cart_payment")
                    cart_payment = CartPayment.objects.create(
                        followBusiness = follow_business,
                        cart_status = cartp['cart_status'],    
                    )
                    
                    if "cart" in cartp:
                        carter = cartp.get("cart")
                        
                        cart = Cart.objects.create(
                            cartPayment = cart_payment,
                            total_price = carter['total_price']
                        )
                        
                        print("cart")
                        print(carter)
                        if "products" in carter:
                            for prod in carter.get("products"):
                                print("productos : --")
                                print(prod)
                                products = Products.objects.create(
                                    cart = cart,
                                    name = prod['name'],
                                    type = prod['type'],
                                    amount = int(prod['amount']),
                                    price = prod['price'],
                                )

                    
                #     print(cart_payment)
                    
            follow_business_list.append({
                "id_conversation": follow_business.id_conversation,
                "type": follow_business.type
            })
        else:
            
            print("No hay follow_business o está vacío.")
                            

        print(user)
        
        clientUserSerizable = ClientUserSerializer(user)
        json_data_client = clientUserSerizable.data
        
        print("User")
        print(clientUserSerizable)
        print(clientUserSerizable.data)
        print(serializable["follow_business"])
        
        

        collection.insert_one(json_data_client)
        conexion.close()


    @classmethod
    def search_user_email(email):
        collection, conexion    =BDConnection.conexion_client_mongo()
       
        user = collection.find_one({"email": email})
        
        conexion.close()
        return user
        
    @classmethod
    def search_id_client(id_client):
        collection, conexion    =BDConnection.conexion_client_mongo()
 
        user = collection.find_one({"idClientChatBot": id_client})
        
        conexion.close()
        return user
    
    def search_user_phone(phone):
        collection, conexion    =BDConnection.conexion_client_mongo()
 
        user = collection.find_one({"phone": phone})
        
        conexion.close()
        return user        
    
class FileContent():
    
    @classmethod
    def upload_logo_business(self,supabase,file,idAdmin:str):
        file_name= f"{idAdmin}/logo_business.jpg"
        file_content = file.read()
        
        try:
            response = supabase.storage.from_('administradores').upload(
                path=file_name,
                file=file_content,
            )
            return True
            
            
        except Exception as e:
            return {"error": str(e)}
    
    @classmethod
    def upload_image_catalog(self,supabase,file,idAdmin:str,index:int):
        file_name= f"{idAdmin}/catalog_business_{index}.jpg"
        file_content = file.read()
        
        try:
            response = supabase.storage.from_('administradores').upload(
                path=file_name,
                file=file_content,
            )
        except Exception as e:
            return {"error": str(e)}
        
        signed_url_data = supabase.storage.from_('admins').create_signed_url(file_name,3600)
        print(signed_url_data)
        
        return {
            "admin_id": idAdmin,
            "signed_url": signed_url_data["signedUrl"],  # ✅ FIX AQUÍ
            "filename": file_name
        }

    
    @classmethod
    def search_image_logo(self,supabase,idAdmin:str):
        try:
            file_name = f"{idAdmin}/logo_business.jpg"
            signed_url = supabase.storage.from_('administradores').create_signed_url(file_name, 3600)
            return signed_url
        except Exception as e:
            return {"error": str(e)}

    
    
    
    
class AiContent:
    @classmethod
    def validation_for_name(cls, user_name, catalog):
        texts = [user_name] + [item["name"] for item in catalog]
        vectorizer = TfidfVectorizer().fit(texts)
        vectors = vectorizer.transform(texts)
        user_vec = vectors[0]
        catalog_vecs = vectors[1:]
        sims = cosine_similarity(user_vec, catalog_vecs)[0]
        best_idx = sims.argmax()
        if sims[best_idx] >= 0.5:
            return catalog[best_idx]
        return None
        
    
    
    
class PayMethodContent():
    @staticmethod
    def get_sdk_mercadopago():
        sdk = mercadopago.SDK(os.environ.get("MERCADOPAGO_ACCESS_TOKEN"))
        return sdk
    
    @classmethod
    def create_yape_token(self,data):
       try:  
            #crea tarjeta de pago
            if not data or 'otp' not in data or 'phoneNumber' not in data:
                return {
                    'status': 400,
                    'error': 'Missing required fields'}
            # Datos capturados desde el frontend
            otp = data["otp"]  # reemplaza por el OTP real
            phone_number = data["phoneNumber"]  # reemplaza por el número real
            request_id = data["requestId"]  # viene de una llamada previa
            idClient = data["idClient"]
            cart_items = data["cart_items"]
            price_total = data["price_total"]
            print(cart_items)
            idConversation = data["idConversation"]
            # notification_url ="https://tusitio.com/webhook/mercado-pago/",
                        
            # URL de la API de Yape
            url = f"https://api.mercadopago.com/platforms/pci/yape/v1/payment?public_key={os.environ.get("MERCADOPAGO_PUBLIC_KEY")}"
            
            print(url)
            # Cuerpo de la solicitud
            payload = {
                "phoneNumber": phone_number,
                "otp": otp,
                "requestId": request_id
                }

            # Encabezados
            headers = {
                "Content-Type": "application/json"
            }

            # Realiza la solicitud
            response = requests.post(url, json=payload, headers=headers)
            # return response.json()

            # Muestra la respuesta
            if response.status_code == 200:
                yape_token = response.json()
                # print(yape_token["id"])

                #Realiza el pago
                sdk = self.get_sdk_mercadopago()   

                request_options = mercadopago.config.RequestOptions()
                request_options.custom_headers = {
                'x-idempotency-key': str(uuid.uuid4())
                }
                
                
                payment_data = {
                    "description": "Carrito de compras de Juan",
                    "installments": 1,
                    "external_reference": "REF-"+ str(idClient),
                    "payer": {
                        "email": "test_user_123@testuser.com",
                        "first_name": "Juan",
                        "last_name": "Pérez",
                        "phone": {
                            "area_code": "01",
                            "number": "987654321"
                        },
                    },
                    "payment_method_id": "yape",
                    "token": yape_token["id"],
                    "transaction_amount": float(price_total),
                    # "notification_url": notification_url,
                    "additional_info": {
                        "items": cart_items,
                        
                    },
                    "notification_url": "https://flexdash.onrender.com/api/payment_notifications/",  # tu webhook
                    
                    "metadata":{
                    
                        "idConversation": idConversation
                    }             

                    }

                payment_response = sdk.payment().create(payment_data, request_options=request_options)
                
                print("Token generado:", yape_token)
                return payment_response
            else:
                # print("Error al generar token:", response.status_code, response.text)
                return {"error": "error el generar token"}
            

            
       except Exception as e: 
           return {"error": str(e)}            


    @classmethod
    def payment_notifications(self ,data):
        try:
            print("Notificación recibida:", data)
            payment_id = data.get("data", {}).get("id")
            if not payment_id:
                return {"status": 400, "error": "Invalid notification format"}

            sdk = self.get_sdk_mercadopago()
            payment_response = sdk.payment().get(payment_id)
            payment = payment_response.get("response", {})
            
            # re = payment.get("response",{})
            metadata = payment.get("metadata",{})
            id_conversation = metadata.get("id_conversation",{})

            print(id_conversation)
            
            
            webhook = os.environ.get("BOTPRESS_WEBHOOK_URL")
            if not webhook:
                return {"status": 500, "error": "BOTPRESS_WEBHOOK_URL no está definido"}

            headers = {"Content-Type": "application/json"}
            print(payment.get("payment_status"))
            print(payment.get("status"))
            if payment.get("status") in ("approved", "rejected"):
                
                payload = {
                    # "response": payment_response,
                    "conversationId": id_conversation,
                    "additional_info":payment.get("additional_info"),
                    "metadata": metadata, 
                    "payment_id": payment_id,
                    "payment_status_details": payment.get("status_detail"),
                    "payment_status": payment.get("status")
                }

                try:
                    response = requests.post(webhook, json=payload, headers=headers, timeout=5)
              
                except requests.RequestException as e:
                    return {
                        "status": 500,
                        "error": f"Fallo al llamar al webhook: {e}",
                        "payment_id": payment_id,
                        "payment_status": payment.get("status")
                    }

                # Intentar parsear JSON de forma segura

                return {
                    "conversationId": id_conversation,
                    "response": payment_response,
                    "status": 200 if 200 <= response.status_code < 300 else response.status_code,
                    "payment_id": payment_id,
                    "payment_status": payment.get("status")
                }

            # Si no es approved ni rejected, no se notifica
            return {
                "status": 200,
                "payment_id": payment_id,
                "payment_status": payment.get("status"),
                "note": "estado no manejado para notificación",
                "p": payment.get("payment_status"),
                "a":payment.get("status")
            }
                
        except Exception as e:
            return {
                'status':500,
                'error': str(e)}
        

    
    
    @classmethod
    def create_payout_mercado_pago(self,cart):
        sdk = mercadopago.SDK(os.environ.get("MERCADOPAGO_ACCESS_TOKEN"))
        # "listProducts" - "listServices"
        
        # for product in cart["listProducts"]:
        
        # for services in  cart["listServices"]:
        combined_items = cart.get("listProducts", []) + cart.get("listServices", [])
        cart_items_Data = []

        for item in cart.get("listProducts", []):
            cart_items_Data.append({
                "title": f"{item['name']} (Producto)",
                "quantity": item["amount"],
                "unit_price": float(item["price"]),
                "currency_id": "PEN"
            })

        for item in cart.get("listServices", []):
            cart_items_Data.append({
                "title": f"{item['name']} (Servicio)",
                "quantity": item["amount"],
                "unit_price": float(item["price"]),
                "currency_id": "PEN"
            })
                
        
        preference_data = {
             "items":cart_items_Data,
            "back_urls": {
                "success": "https://tusitio.com/payment-success/",
                "failure": "https://tusitio.com/payment-failure/",
                "pending": "https://tusitio.com/payment-pending/"
            },
            "auto_return": "approved",  # para redirigir automáticamente al success
            "notification_url": "https://tusitio.com/webhook/",  # tu webhook
            "external_reference": "pedido_12345",  # opcional
        }
  
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        print(preference_data["items"])

        return JsonResponse({"init_point": preference["init_point"]})


    
    

class TestContent():
    @classmethod
    def test_webhook(self, data):
        
        webhook = os.environ.get("BOTPRESS_WEBHOOK_URL")
     
        payload= {
            "conversationId": data["conversationId"],
            "metadata": data["metadata"]
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(webhook, json=payload, headers=headers, timeout=5)
        
        print(response)
        
        return {
            "response": payload
        }
    
    
class CalContent():
    
    @classmethod
    def verification_time_zone(self,date_str:str,default_year:int):
        try:
            print(date_str)
            print(default_year)
        
            result = {
                "success": False,
                "parsed_date": None,  # será un objeto date si es válido
                "message": ""
            }

            if not isinstance(date_str, str) or not date_str.strip():
                result["message"] = "Fecha debe ser una cadena no vacía."
                return result

            today = datetime.now(tz=ZoneInfo("America/Lima")).date()

            # Limpia entrada de espacios y slashes extremos
            cleaned = date_str.strip().strip("/")
            parts = cleaned.split("/")

            if len(parts) == 2:
                cleaned = f"{cleaned}/{default_year}"
            elif len(parts) == 3:
                pass  # ya viene con año
            else:
                result["message"] = "Formato inválido: debe ser 'DD/MM' o 'DD/MM/YYYY'."
                return result

            try:
                parsed = datetime.strptime(cleaned, "%d/%m/%Y").date()
            except ValueError as e:
                result["message"] = f"Fecha inválida: {e}"
                return result

            if parsed < today:
                result["parsed_date"] = parsed
                result["message"] = "La fecha ya pasó."
                return result

            result["success"] = True
            result["parsed_date"] = parsed
            result["message"] = "Fecha válida."
        
            return result
        except Exception as e:
            return {
                "error": e
            }
    
    @classmethod    
    def resave_total_price(cls, payload):
        if not isinstance(payload, dict):
            return JsonResponse({"status": 400, "error": "payload debe ser un objeto JSON"}, status=400)

        # validar campos esenciales
        id_business = payload.get("idBusiness")
        if not id_business:
            return JsonResponse({"status": 400, "error": "idBusiness faltante"}, status=400)
        try:
            default_year = int(payload.get("default_year", 0))
        except Exception:
            return JsonResponse({"status": 400, "error": "default_year inválido"}, status=400)

        price_total = Decimal("0.0")
        jsonCatalog = AdminContent.search_id_catalog(id_business)
        if jsonCatalog is None:
            return JsonResponse({
                "status": 404,
                "response": {"error": "catálogo del negocio no encontrado"}
            }, status=404)

        def validate_and_accumulate(item, expected_type):
            nonlocal price_total
            if not isinstance(item, dict):
                return JsonResponse({"status": 400, "response": {"error": f"item inválido en {expected_type}"}}, status=400)

            title = item.get("title")
            if not title:
                return JsonResponse({
                    "status": 404,
                    "response": {"error": f"{expected_type} sin título proporcionado"}
                }, status=404)

            obj = AiContent.validation_for_name(title, jsonCatalog)
            if not isinstance(obj, dict) or obj.get("type") != expected_type:
                return JsonResponse({
                    "status": 404,
                    "response": {"error": f"{expected_type} '{title}' no válido o no encontrado"}
                }, status=404)

            # Normalizar campos
            item["title"] = obj.get("name", title)
            item["unit_price"] = obj.get("price", "0.0")

            if expected_type == "serv":
                date_str = item.get("date", "")
                time_str = item.get("time", "")
                
                #validar fechas
                result = cls.verification_time_zone(date_str=date_str,default_year= default_year)
                if result.get("success"):
                    print(result)
                    item["description"] = f"fecha registrada: {date_str} - Hora: {time_str}"
                else:
                    return JsonResponse({
                        "status": 404,
                        "response": {"error": f"Fecha pasada es invalida"}
                    }, status=404)
                    # item["description"] = "fecha ya pasada invalida"
                #validar por carrito de compras
            else:  # prod
                item["description"] = obj.get("description", "")

            quantity = int(item.get("quantity", 1))
            unit_price = Decimal(str(obj.get("price", "0.0")))
            price_total += unit_price * quantity
            return None  # indica éxito

        # Procesar servicios
        for service_item in payload.get("listServices", []):
            err = validate_and_accumulate(service_item, "serv")
            if isinstance(err, JsonResponse):
                return err

        # Procesar productos
        for product_item in payload.get("listProducts", []):
            err = validate_and_accumulate(product_item, "prod")
            if isinstance(err, JsonResponse):
                return err

        payload["price_total"] = str(price_total)
        return JsonResponse({"status": 200, "response": payload}, status=200)
             
             

        # print("calMethod")
        # print(jsonCatalog)
        # print("LOLOOLOO JAKJSKAJKSK LOLOLOLOL")

        #     for user_product in json["listProducts"]:  # Producto que viene del usuario
        #         for item in jsonCatalog:  # Productos del catálogo
        #                 # Comparación flexible (ignorando mayúsculas/minúsculas)
        #             if item["name"].lower() in user_product["name"].lower():
        #                 user_product["name_real"] = item["name"]
        #                 AiContent.validation_for_name()
        #                 user_product[""]
        #                 user_product["price"] = item["price"]
            
        # try: 
            
        #     print("precio_total")
        #     print(price_total)
            
        #     print("💲 Precio total calculado:", price_total)
            



            
        # except Exception as e:
        #      return JsonResponse({
        #          "status": 400,
        #          "error": str(e),
        #      })
             
             
             
        # jsonProducts = {
        #     "name": 
        #     "type":
        #     "price":
        #     "amount"
        # }
        
        # jsonServices = {
        #     "name": 
        #     "type":
        #     "price":
        #     "amount"
        # }
        
            
            # for services in json ["listServices"]
        # data= {
        #     "listServices": 
        #     "listProducts":
        #     "totalPrice": price 
        # }
        
class  TicketsContent():
    
    @classmethod
    def create_tickets(self, ticketload):
    
        collection, conexion = BDConnection.conexion_client_mongo()

        collection.insert_one(ticketload)
        conexion.close()

        # ticketload={
            
        #     "idClient":"",
        #     "idBusiness":"",
        #     "idTicket":"",
        #     "idTransferencia":"",
        #     "cart_item":"",
        #     "price_total":0,
        #     "metadata":{
                
        #        "name":"",
        #        "phoneNumber":0,
        #        "email":"",
        #     },
        #     "qr":"",
        #     "date":""            ,
        # }
        
    def ticket_to_img():
        pass

class utilsContent():
    def make_qr_with_url(base_url: str, id_business: str, id_boleta: str) -> str:
        """
        Construye la URL de checkout y genera el QR como data URI.
        Ejemplo resultante: https://mi-dominio.com/checkout_ticket_url/123/456/
        """
        # Asegura que no haya doble slash
        path = f"checkout_ticket_url/{urllib.parse.quote(id_business)}/{urllib.parse.quote(id_boleta)}/"
        full_url = urllib.parse.urljoin(base_url.rstrip("/") + "/", path)  # mantiene scheme+host

        # Generar QR de la URL
        import qrcode, io, base64
        qr = qrcode.QRCode(box_size=4, border=1)
        qr.add_data(full_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{b64}", full_url
