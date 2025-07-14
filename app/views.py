import requests
import base64
import certifi
import json


from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from django.conf import settings



from django.core import serializers
# from .models import Client

#importacion de dependecias utils
from datetime import datetime
import uuid

# clientes = Client.objects.all()
# data = serializers.serialize('json',clientes)












class BDConnection():

    #bot normal 25 - bot confuncionalidades IA 40- bot personalizable 85
    def connection_mongo():

        client = MongoClient(settings.MONGO_ATLAS_KEY, 
                            server_api=ServerApi('1'), 
                            tlsCAFile= certifi.where())

        print(client)

        print(f"conexion exitosa con {client}")
        return client


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
def add_user(request):
    if request.method == "POST":
        try:
            #informacion del json enviado por el POST
            data = json.loads(request.body)
            
            #propiedades que obtendre del post
            idClientChatBot = data.get('idClientChatBot')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            phone = data.get('phone')
            country = data.get('country')
            uid = f"user-{datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:6]}"

            # Si alguno está vacío o no viene, lanzar error
            if not first_name or not email or not phone:
                return JsonResponse({
                    'status': 400,
                    'response': "Datos incompletos o incorrectos"
                }, status=400)
            
            #Json del servidor Serializable
            clientSerializable = {
                "idClient": uid,
                "idClientChatBot": idClientChatBot,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "type_business": [],
                "country": country,
                "date": datetime.now()
            }

            # nombre = data.get('name','')
            
            # edad = data.get('edad',0)
            # json_data = json.loads(json_header)
            # print("Los datos son: " + str(json_data))

            # Insertar en Mongo
            client = BDConnection.connection_mongo()
            db = client['flexDash']
            collection = db['client']
            collection.insert_one(clientSerializable)
            

            client.close()

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
    client = BDConnection.connection_mongo()
    if request.method == "GET":
        try:
            db = client['flexDash']
            collection = db['collection']
            # data = json.loads(request.body)
            # print(data)


            # idClientChatBot = data.get('idClientChatBot','')

            IdClientChatBot = request.GET.get('IdClientChatBot')


            # print(id_user)

            if collection.find_one({"idUser": IdClientChatBot}):
                

                return JsonResponse({"response": {"text": "Esta cuenta esta registrada","value":True}},status=201)
            else:
                return JsonResponse({"response": {"text":"Esta cuenta no esta registrada","value":False}}, status = 201)
        except Exception as e:
            return JsonResponse({'error': str(e)},status = 400)
    client.close()
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