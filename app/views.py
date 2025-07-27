import requests
import base64
import json
import os
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings



from django.core import serializers
# from .models import Client

#importacion de dependecias utils
import uuid
from supabase import create_client
from app.content import ClientContent ,AdminContent,FileContent, CalContent


# clientes = Client.objects.all()
# data = serializers.serialize('json',clientes)


supabase = create_client(os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_KEY'))

@csrf_exempt
def upload_image_to_supabase(request):
    if request.method == 'POST':
        file = request.FILES.get('imagen')  # En Django, por ejemplo
 
        #LAS IMAGENES NO VAN EN EL JSON (URL PUBLICAS / STR)       
        json = FileContent.search_image_logo(supabase, idAdmin="12389283")    
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
def cal_price_total (request):
    if request.method == 'POST':
        try:

            data = json.loads(request.body)

            print(data)

            response = CalContent.resave_total_price(data)  
            print(response)
            
            return JsonResponse(data)   
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





@csrf_exempt
def add_admin(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            AdminContent.add_user(data)
            
            if data :
                return JsonResponse({
                'status': 200,
                'response': {
                    "data":str(data)
                    },
                # "title": "Datos subidos desde body a la BD"
        }, status=201)
        except Exception as e:
            return JsonResponse({
            'status': 400,
            'response': "datos incompletos."
            ,'error': str(e)}, status=400)
            


@csrf_exempt
def add_user(request):
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
def validation_user(request):
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



def encode_image(filename):
    with open(filename, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")




@csrf_exempt 
def search_for_id_user():
    #  try:
    
    #  except:

        return "a",




def index(request):
    return HttpResponse("Hola a todos los que operan en este servicio")



import mercadopago


sdk = mercadopago.SDK(os.environ.get('MERCADOPAGO_ACCESS_TOKEN'))

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