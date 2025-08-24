import requests
import base64
import json
import os
from pathlib import Path

from datetime import datetime
from django.utils import timezone
import hmac
import hashlib
from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, FileResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie,requires_csrf_token


from app.content.orders import OrdersManager


from django.core import serializers
# from .models import Client

#importacion de dependecias utils
import uuid
from app.content.api import ClientContent, CalContent,PayMethodContent,TestContent,TicketsContent,utilsContent,LoadContent
from app.content.file import FileContent
from app.content.business import BusinessManager
from app.content.admin import AdminContent
from app.content.auth  import AuthContent

# from app.services.analytics import AnalyticsOrders
# import app.content.api

# clientes = Client.objects.all()
# data = serializers.serialize('json',clientes)



# def extraer_csrf_de_cookie_header(cookie_header: str) -> str | None:
#     cookies = cookie_header.split(';')
#     for cookie in cookies:
#         key_value = cookie.strip().split('=')
#         if len(key_value) == 2 and key_value[0] == 'csrftoken':
#             return key_value[1]
#     return None

# @requires_csrf_token
# def csrf_failure(request, reason=""):
#     print(request.body)
#     print("CSRF error:", reason)
#     return redirect('/get-csrf/')  # o tu página de inicio de sesión

@ensure_csrf_cookie
def get_csrf_token(request):
    print(request.GET.get("next", "/"))
    print(request.COOKIES.get("csrftoken"))
    # request.headers.get("X-CSRFTOKEN") = request.COOKIES.get("csrftoken")
   
    # Dom / A / url
   
    return JsonResponse({'message': 'CSRF cookie set correctamente.'})


def login_admin(request):
#   get_csrf_token()    

  if request.method == "POST":
        try:
            print(request.headers.get("Cookie"))

            data = json.loads(request.body)
            
            
            serial = data.get("auth")   
            
            response = AuthContent.login_admin(request=request,data=serial)
            
            if data :
                return JsonResponse({
                'status': 200,
                'CSFR': request.headers.get("X-CSRFToken"),
                'response': {
                    "data":data
                    },
                # "title": "Datos subidos desde body a la BD"
            }, status=201)
            return JsonResponse({'success': f'Superusuario {response} creado correctamente'})     
                
        except Exception as e:
            
            return JsonResponse({
            "LOL":"A",
            'status': 400,
            'response': "datos incompletos."
            ,'error': str(e)}, status=400)
        
              


@csrf_exempt
def reg_admin(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        
            print(request.FILES.get("logo",""))
           
            
            if request.method != 'POST':
                return JsonResponse({"response", "No es posible obtener vistas"})

            response = AuthContent.reg_admin(data)
            
            if response:
             return response
            
            if data :
                return JsonResponse({
                'status': 200,
                'response': {
                    "data":data
                    },
                # "title": "Datos subidos desde body a la BD"
            }, status=201)
                
        except Exception as e:
            return JsonResponse({
            'status': 400,
            'response': "datos incompletos."
            ,'error': str(e)}, status=400)
            

def reg_business(request):
    if request.method != "POST":
        return JsonResponse({
            'status':404,
            'error': f'Metodo Invalido {request.method}'
        })
        
    try:
        id_admin = request.headers.get('Id-Admin')
        print(id_admin)
        data = json.loads(request.body)
        response = BusinessManager.reg_business(id_admin, data)
                
        if data :
            return JsonResponse({
            'status': 200,
            'response': {
                "message":"Datos sunidos correctamente"
                # "data": data
                },
            # "title": "Datos subidos desde body a la BD"
        }, status=201)
            
    except Exception as e:
        return JsonResponse({
        'status': 400,
        'response': "datos incompletos."
        ,'error': str(e)}, status=400)




@csrf_exempt
def upload_logo_business(request):
    if request.method == 'POST':
        file = request.FILES.get('logo')  # En Django, por ejemplo
 
        #LAS IMAGENES NO VAN EN EL JSON (URL PUBLICAS / STR)       
        json = FileContent.upload_logo_business( idAdmin="12389283")    
        print(json)
        
        
        if json:
            return JsonResponse({
                "status": 200,
                "response": "imagen subida "   
            })
        return JsonResponse({
            "status": 200,
            "response": " imagen nosubida "   
        })

    return JsonResponse({
        "status": 200,
        "response": f"Metodo no valido:  {requests.method}"   
    })
    
    
def upload_catalog_to_business(request):
    if request.method == "POST":
        file = request.Files.get('catalog')

    
    
# def get_public_url(filename):
#     url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(filename)
#     return url['data']['publicUrl']


# def get_signed_url(filename, expires_in=60):
#     url = supabase.storage.from_(settings.SUPABASE_BUCKET).create_signed_url(filename, expires_in)
#     return url['data']['signedUrl']




# def subir_imagen_admin(file):

#     admin_id = str(uuid.uuid4())
#     filename = f"{admin_id}/catalog_business.jpg"
#     file_content = file.read()

#     try:
#         response = supabase.storage.from_("administradores").upload(
#             path=filename,
#             file=file_content
#         )
#     except Exception as e:
#         return {"error": str(e)}

#     # Obtener URL firmada de forma correcta usando .data
#     signed_url_data = supabase.storage.from_("administradores").create_signed_url(filename, 3600)
#     print(signed_url_data)

#     return {
#         "admin_id": admin_id,
#         "signed_url": signed_url_data["signedUrl"],  # ✅ FIX AQUÍ
#         "filename": filename
#     }

# @csrf_exempt
# def add_admin(request):

        
    
    

@csrf_exempt
def add_business():
    
    if requests.method == 'POST':
        file = requests.Files['imagen']
        
        
        
        # result = upload_image_to_supabase(file)
        # return JsonResponse(result)
    return JsonResponse({"error": "No se envio imagen"}, status=400)

#Admin
#Business
#Catalog






@csrf_exempt
def subir_catalogo_admin(request):
    if request.method == 'POST' and 'imagen' in request.FILES:
        file = request.FILES['imagen']
        resultado = subir_imagen_admin(file)
        return JsonResponse(resultado)

    return JsonResponse({"error": "No se envió imagen"}, status=400)

        

def get_error(request):
    return JsonResponse({
        'error': 'Este endpoint siempre falla.',
        'code': 'FORCED_ERROR'
    }, status=400)  # o 500 si quieres un error de servidor

def get_json_test(request): 
    # print(data)
    data = {}
    return JsonResponse(data)


# Create your views here.
# Vista para enviar JSON como peticion
@csrf_exempt
def obtener_post_pagina(request):
    url = 'https://jsonplaceholder.typicode.com/posts'
    data = {
    "title": "Nuevo post",
    "body": "Este es el contenido",
    "userId": 1
    }
    
    if request.method == 'POST':
        response = requests.post(url,json=data)
        return JsonResponse({"response": f"informacion enviada correctamente {response}"}, status=200)
    else :
        return JsonResponse({"error": "error al realizar el post"})
    
def obtener_pots(request):
    url = 'https://jsonplaceholder.typicode.com/posts'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        return JsonResponse(data,safe=False)
    else:
        return JsonResponse({'error': 'Nose pudo obtener los datos'}, status=500)

@csrf_exempt
def resave_item_order (request):
    if request.method == 'POST':
        try:

            data = json.loads(request.body)

            print(data)

            response = CalContent.resave_total_price(data)  
            print(response)
            
            return response
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
      


def recibir_dato(request):

    if request.method == 'POST':
        try:
            # Si recibes JSON:
            data = json.loads(request.body)
            nombre = data.get('name', '')
            edad = data.get('edad', 0)

            # Aquí puedes guardar en BD, procesar, etc.
            respuesta = {
                'mensaje': f'Hola {nombre}, tienes {edad} años',
                'datos_recibidos': data
            }
            return JsonResponse(respuesta)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)



@csrf_exempt
def add_catalog(request):
    if request.method =="POST":
        try:
            data = json.loads(request.body)
            
            
            catalog = [
                        {
                            "name": "Nombre",
                            "description": "",
                            "type": "prod - serv",
                            "price": 0.0,
                            "stock": 0
                        }
                    ],
            return JsonResponse(
                {   "status": 200,
                    "response" :"Catalogo del nDatos agregados corretamente"
                },status=200
            )
        except Exception as e:
             return JsonResponse(
                {   "status": 400,
                    "error" : f"Error al guardar los datos: {e}"
                },status=400
            )
    return JsonResponse({"status":400,"error":"Error dentro del codigo"},status=400)

def upload_orders_view(request):
    OrdersManager.upload_orders()
    return JsonResponse({"status": "ok"})


            


@csrf_exempt
def add_client(request):
        #validacion errores
    if request.method == "POST":
        try:
            
            # imagen = request.POST.get("imagen")
            
            #informacion del json enviado por el POST
            data = json.loads(request.body)
            # conexion_client_mongo()
            #propiedades que obtendre del post
            first_name = data.get('first_name')
            email = data.get('email')
            phone = data.get('phone')


            follow_business = data.get('follow_business')
            
            # Si alguno está vacío o no viene, lanzar error
            if not first_name or not email or not phone:
                return JsonResponse({
                    'status': 400,
                    'response': "Datos incompletos o incorrectos"
                }, status=400)

            ClientContent.add_user(data)
            
            # validar Email
            
            # nombre = data.get('name','')
            
            # edad = data.get('edad',0)
            # json_data = json.loads(json_header)
            # print("Los datos son: " + str(json_data))

            # Insertar en Mongo
            return JsonResponse({
                'status': 200,
                'response': str(data),
                "title": "Datos subidos desde body a la BD"
            }, status=201)

        except Exception as e:
            return JsonResponse({
                'status': 400,
                'response': "datos incompletos."
                ,'error': str(e)}, status=400)

    return JsonResponse({'status': 405,'error': f'Método no permitido : {request.method}'}, status=405)


@csrf_exempt
def validate_client(request):
    if request.method == "GET":
        try:
            phone = request.GET.get('phone')
            # id_client = request.GET.get('IdClientChatBot')
            # email = request.GET.get('email')
            # if not id_client:
            #     return JsonResponse({'error': 'Parámetro IdClientChatBot requerido'}, status=400)
            # user_exists_id = ClientContent.search_id_client()
            
            user_exists_phone   = ClientContent.search_user_phone(phone)
            # if user_exists_id or user_exists_email:
            if user_exists_phone:
                return JsonResponse({
                    "validate": True,
                    "response": {"text": "Esta cuenta está registrada", "value": True}
                }, status=200)
            else:
                return JsonResponse({
                    "validate": False,
                    "response": {"text": "Esta cuenta no está registrada", "value": False}
                }, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
      
    return JsonResponse({'error': f'Método no permitido: {request.method}'}, status=405)

@csrf_exempt
def get_id_client(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            idClient = data.get("idClientChatBot") 
            
            response = ClientContent.search_id_client(idClient)
            
            if response is None:
                    
                return JsonResponse({
                    "response": {"text": "cliente no encontrado"}
                },status=200)
            
            return JsonResponse({
                "response": response
            },status=200)
            
            
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': f'Método no permitido: {request.method}'}, status=405)




def encode_image(filename):
    with open(filename, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def create_order(add_order):
    A



@csrf_exempt 
def search_for_id_user():
    #  try:
    
    #  except:

        return "a",




def index(request):
    return HttpResponse("Hola a todos los que operan en este servicio")



import mercadopago


# sdk = mercadopago.SDK(os.environ.get('MERCADOPAGO_ACCESS_TOKEN'))

@csrf_exempt
def crear_pago(request):
    
    
    preference_data = {
        "items": [
            {
                "title": "Producto de prueba",
                "quantity": 1,
                "currency_id": "PEN",  # Moneda peruana
                "unit_price": 50.0
            }
        ],
        "back_urls": {
            "success": "https://tusitio.com/pago-exitoso",
            "failure": "https://tusitio.com/pago-fallido",
            "pending": "https://tusitio.com/pago-pendiente"
        },
        "auto_return": "approved"
    }
    
    

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

    return JsonResponse(preference_response)

def validation_pago():
    {
        
    }
def test_webhook_botpress():
    url = "https://webhook.botpress.cloud/8481047b-5c05-4f41-b1df-51e31a4323e7"

    payload = {
        "type": "text",
        "text": "texto de prueba",
        "userId": "8481047b-5c05-4f41-b1df-51e31a4323e7",
        "channel": "webhook"  # debe coincidir con el canal en Botpress
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.status_code, response.text


def payment_methods(request):
    # Devuelve métodos de pago habilitados
    ...
@csrf_exempt
def create_checkout_session(request):
    
    cart =json.loads(request.body)

    
    # Crea un link de pago o preferencia
    if request.method == "POST":
        checkout = PayMethodContent.create_payout_mercado_pago(cart=cart)
        return checkout
    else:
        
        return JsonResponse({"error": "Método no permitido"}, status=405)
    ...

def payment_success(request):
    # Página de confirmación
    ...

def payment_failure(request):
    # Página de error
    ...

def payment_pending(request):
    # Página cuando el pago no fue confirmado aún
    ...

@csrf_exempt
def payment_webhook(request):
    # Escucha eventos del proveedor de pagos
    ...

def payment_status(request, order_id):
    # Consulta el estado del pago desde el backend
    ...
    
def payment_success(request):
    return render(request, 'payments/success.html')

def payment_failure(request):
    return render(request, 'payments/failure.html')

def payment_pending(request):
    return render(request, 'payments/pending.html')


@csrf_exempt
def create_yape_payment(request):
    if request.method == "POST":
        try:            
            data = json.loads(request.body)  
            print(data)
            response = PayMethodContent.create_yape_token(data)
            return JsonResponse(response)
        
        except Exception as e:
            return JsonResponse({"status": 400,"error":e})
    else: 
        return JsonResponse({"response": "metodo no permitido: "+ request.method })


@csrf_exempt
def payment_notifications(request):
    if request.method == "POST":
        try:
            client_secret = os.environ.get("CLIENT_SECRET")
            header = request.headers.get("x-signature")

            print(header)
            
            #   # Procesar notificaciones de webhook
            # # if received_signature:
            # #     generated_signature = "sha256=" + hmac.new(client_secret, request.body, hashlib.sha256).hexdigest()
                
            # #     if hmac.compare_digest(received_signature, generated_signature):
                    
            # #         return True  # La firma es válida
            # #     return False  # Alguien alteró el contenido o no es de Mercado Pago
            
            
            
                    # return JsonResponse({"error": "No se recibió el header 'x-signature'"}, status=400)
            if  header :

                # Extrae ts y v1
                parts = dict(part.split("=") for part in header.split(",") if "=" in part)
                ts = parts.get("ts")
                v1 = parts.get("v1")

                print(parts)
                if not ts or not v1:
                    return JsonResponse({"error": "Firma inválida (faltan partes)"}, status=400)

                # Cuerpo en bytes
                raw_body = request.body

                # Genera firma local
                to_sign = f"{ts}.{raw_body.decode()}".encode()
            
                print(to_sign)
                local_signature = hmac.new(client_secret, to_sign, hashlib.sha256).hexdigest()
                verification = hmac.compare_digest(local_signature, v1)
                if not hmac.compare_digest(local_signature, v1):
                    return JsonResponse({"error": "Firma inválida"}, status=403)
                print(f"firma verificada {verification}")

            
            data = json.loads(request.body)
            response = PayMethodContent.payment_notifications(data=data)
            return JsonResponse(response, status=200)  # ✅ Estado 200 explícito
        
        except Exception as e:
            return JsonResponse({"status": 400,"error": str(e)})
    else: 
        return JsonResponse({"response": "metodo no permitido: "+ request.method })
    
    
    

@csrf_exempt
def generate_ticket_html(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Solo POST válido")

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": 400, "error": "JSON inválido"}, status=400)

    context = LoadContent.ticket_payload(payload)

    base_url = request.build_absolute_uri("/")  # para resolver assets relativos

    qr_data_uri, target_url = utilsContent.make_qr_with_url(base_url, context.get("id_business"), context.get("id_boleta"))
    context["qr_data_uri"] = qr_data_uri
    context["checkout_url"] = target_url  # opcional para depuración


    output_param = request.GET.get("output", "png").lower()  # "png" por defecto

    response = utilsContent.html_to(context=context,output_param=output_param,base_url=base_url)

    print(response)
    
    
    return response





def checkout_ticket(request, id_business, id_boleta):
    # Aquí haces lo que necesites: mostrar la boleta, validar, pagar, etc.
    return HttpResponse(f"Checkout para negocio {id_business}, boleta {id_boleta}")

