import requests
import base64

from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient 
import json



from PIL import Image, ImageDraw , ImageFont

def generate_image(request):
    imagen= Image.new('RGB',(1920,1080),color='white')

    dibujo = ImageDraw.Draw(imagen)
    dibujo.rectangle([0, 0, 200, 50], fill='blue', outline='black')
    # Cargar una fuente y establecer el tamaño (por ejemplo, 30)
    fuente = ImageFont.truetype("arial.ttf", 200)  # Cambia por otra si no tienes Arial


    dibujo.text((10, 30), "Hola este es mi", font=fuente, fill="black")
    imagen.save('imagen_generada.png')

    return JsonResponse({'response': 'ok respuesta procesada'})


# Create your views here.
def obtener_pots(request):
    url = 'https://jsonplaceholder.typicode.com/posts'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        return JsonResponse(data,safe=False)
    else:
        return JsonResponse({'error': 'Nose pudo obtener los datos'}, status =500)


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
            # Obtener el JSON como string desde el header
            # json_header = request.headers.get("JSON")  # 👈 esto es un string
            # print(json_header)
            # Convertir de string a dict
            # json_body = request.body
            # print(json_body)
            data = json.loads(request.body)
            nombre = data.get('name','')
            edad = data.get('edad',0)

            # json_data = json.loads(json_header)
            # print("Los datos son: " + str(json_data))

            # Insertar en Mongo
            client = connection_mongo()
            db = client['flexDash']
            collection = db['collection']
            collection.insert_one(data)
            

            client.close()

            return JsonResponse({
                'response': str(data),
                "title": "Datos subidos desde header a la BD"
            }, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': f'Método no permitido : {request.method}'}, status=405)

@csrf_exempt
def validation_user(request):
    client = connection_mongo()
    if request.method == "POST":
        try:
            db = client['flexDash']
            collection = db['collection']
            data = json.loads(request.body)
            print(data)

            id_user = data.get('idUser','')



            print(id_user)

            if collection.find_one({"idUser": id_user}):
                

                return JsonResponse({"response": {"text": "Esta cuenta esta registrada","value":True}},status=201)
            else:
                return JsonResponse({"response": {"text":"Esta cuenta no esta registrada","value":False}}, status = 201)
        except Exception as e:
            return JsonResponse({'error': str(e)},status = 400)
    client.close()
    return JsonResponse({'error': f'Método no permitido: {request.method}'}, status=405)

def connection_mongo():
    username = "gespinoza12"
    password = "ges12"
    

    client = MongoClient(f'mongodb+srv://{username}:{password}@flexdash.pqxf1mp.mongodb.net/?retryWrites=true&w=majority&appName=flexdash')

    print(client)

    print(f"conexion exitosa con {client}")
    return client


    # for doc in collection.find({"hobby": {"$exists" : True}}):
    #     print(doc)



    # collection.delete_many({"hobby": {"$exists": True}})







    # document ={
    #     "name": "usuario1",
    #     "edad": 12,
    #     "city": "SAS",
    #     "hobby": "guitarra",
    # }



    # list_document = [
    #     {"name": "usuario1",
    #       "idUser": 3182947923,  
    #      "edad": 12,
    #      "hobby": "guitarra",},
    #     {"name": "usuario2",
    #      "idUser":3182944231,
    #      "edad": 24,
    #      "hobby": "flauta",
    #      },
    #     {"name": "usuario3",
    #      "idUser": 3182944321,
    #      "edad": 32,
    #      "hobby": "play", 
    #      },
    # ]


    # header = {
    #     "Content-Type": "application/json",
    # }


    # # insertdoc =collection.insert_one(document)
    # insertMany = collection.insert_many(list_document)

    # print(f"documento insertado con exito: {list_document.index}")
    

    # client.close()
    # return JsonResponse({"response": "envio de datos Exitoso"})
    
    #emprendedor
    #usuario
    #productos


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