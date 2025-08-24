from app.conexion import BDConnection
from django.http import JsonResponse
import json
from datetime import datetime
import uuid

class AdminContent():
    @classmethod
    def add_user(self, serializable:json):
        collection ,conexion= BDConnection.conexion_admin_mongo()
        
        print("Campo-SEriizable")
        print(serializable)
        print("Campo-SEriizable")
        
        # #creacion modelo 
        # # Datos del Admin
        # user = AdminUser.objects.create(
        #     full_name=serializable["full_name"],
        #     first_name=serializable["first_name"],
        #     last_name=serializable["last_name"],
        #     dni=serializable["dni"],
        #     phone=serializable["phone"],
        #     country=serializable["country"],
        #     email=serializable["email"],
        # )
        
        # print(user.full_name)
        
        # print(serializable["business"])
        
        # if "business" in serializable:
        #     for b in serializable.get("business"):
        #         print("business")
                
        #         business = Business.objects.create(
        #             AdminUser=user,
        #             idBot=b['idBot'],
        #             name=b['name'],
        #             category=b['category'],
        #             ruc=b['ruc'],
        #             phone_number=b['phone_number'],
        #             phone_country_code=b['phone_country_code'],
        #             catalog_url=b['catalog_url'],
        #             description=b['description'],
        #             address=b['address'],
        #             logo_url=b['logo_url']
        #         )

        #         print(business)  # ✅ Ahora sí existe

        #         if "catalog" in b:
        #             bc = b["catalog"]
        #             catalog = Catalog.objects.create(
        #                 business=business,
        #             )
        #             print(catalog)

        #             # Creamos imágenes
        #             if "catalog_images" in bc:
        #                 for catalog_image in bc["catalog_images"]:
        #                  catalog_image_object= CatalogImage.objects.create(
        #                         catalog=catalog,
        #                         name=catalog_image["name"],
        #                         type=catalog_image["type"],
        #                         img_url=catalog_image["img_url"]
        #                     )
        #             # Creamos items
        #             if "catalog_items" in bc:
        #                 for catalog_item in bc["catalog_items"]:
        #                     print(catalog_item)
        #                     print(catalog_item["price"])
        #                     CatalogItem.objects.create(
        #                         catalog=catalog,
        #                         name=catalog_item["name"],
        #                         description=catalog_item.get("description", ""),
        #                         type=catalog_item["type"],
        #                         price=catalog_item["price"],
        #                         stock=catalog_item["stock"]
        #                     )

        #             # ✅ Serializamos el catálogo recién creado (con imágenes e items ya guardados)
        #             catalog_serializer = CatalogSerializer(catalog)
        #             b["catalog"] = catalog_serializer.data


        #         if "method_payment" in b:
        #             mp = b["method_payment"]
        #             MethodPayment.objects.create(
        #                     business=business,
        #                     type=mp["type"],
        #                     name=mp["name"],
        #                     lastName=mp.get("lastName", ""),
        #                     email=mp.get("email", ""),
        #                     phone=mp.get("phone", ""),
        #                     phone_number=mp.get("phone_number", ""),
        #                     country_code=mp.get("country_code", ""),
        #                     qrImageUrl=mp.get("qrImageUrl", ""),
        #                     account_token=mp.get("account_token", ""),
        #                     public_key=mp.get("public_key", "")
        #                 )
                
        #             print("social_media")

        #         if "social_media" in b:
        #             for sm in b["social_media"]:
        #                 print(sm)
        #                 SocialMedia.objects.create(
        #                     business=business,
        #                     type_social=sm["type_social"],
        #                     urlPage=sm["urlPage"]
        #                 )

        #         if "co_workers" in b:
        #             for cw in b["co_workers"]:
        #                 # cw = serializable["co_workers"] 
        #                 CoWorker.objects.create(
        #                     business=business,
        #                     coworker_id=cw.get("coworker_id", ""),
        #                     status=cw.get("status", "")
        #                 )

        #         if "feedback" in b:
                    
        #             for  fb in b["feedback"]:
                    
        #                 Feedback.objects.create(
        #                     business=business,
        #                     name=fb["name"],
        #                     message=fb.get("message", "")
        #                 )

        #         if "time_zone" in b:
        #                 tz = b["time_zone"]
        #                 TimeZone.objects.create(
        #                     business = business,
        #                         time_open = tz["time_open"],
        #                         time_close = tz["time_close"]
        #                 )
            
        # adminUserSerializer = AdminUserSerializer(user)
        # json_data = adminUserSerializer.data

        # print("parte final")
        # print(json_data)
        
        
        # for business in serializable["business"]:
        #     business["id"] = str(uuid.uuid4())
        #     business["date"] = datetime.now()
        
        # serializable["id"] = str(uuid.uuid5(uuid.NAMESPACE_DNS,"email"))
        
        
        serializable["orders"] = []
        serializable["date"] = datetime.now()
        response = collection.insert_one(serializable)
        
        

        conexion.close()
        return str(response.inserted_id) , serializable
        
    @classmethod
    def get_user_id(self, id:str):
        try:
            collection, conexion = BDConnection.conexion_admin_mongo() 
            doc = collection.find_one({"id":id,},{"_id": 0})
            
            # Convierte datetimes a str automáticamente
            doc_str = json.loads(json.dumps(doc, default=str))
            
            print(doc_str)
            if doc_str:
            # bson.json_util.dumps convierte el documento (incluyendo UUID/ObjectId) a JSON válido
                conexion.close()
                return doc_str
            else:
                return {
                    "status":404,
                    "error": "usuario no encontrado"}

        except Exception as e:
            return {
                "Error": str(e),
            }
        
    @classmethod
    def search_id_catalog(cls, id):
        collection, conexion = BDConnection.conexion_admin_mongo()

        try:
            # Buscar documento con ese ID
            doc = collection.find_one({"id": id})
            print(doc)
            if not doc:
                return JsonResponse({
                    "status": 404,
                    "message": "Documento no encontrado"
                })

            # Asegurar que 'catalog' y 'catalog_items' existan
            # catalog = doc.get("business", [])[0].get("catalog") if doc.get("business") else None
            # catalog_items = catalog.get("catalog_items") if catalog else None

            # print("catalog - Business")
            print(doc)
            
            return doc
            

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
            
            
