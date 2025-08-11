from app.conexion import BDConnection
from django.http import JsonResponse
import json
from datetime import datetime
import uuid

class BusinessContent():
    
    @classmethod
    def reg_business(self,idAdmin,serializable):
        # def add_user(self, serializable:json):
        collection ,conexion= BDConnection.conexion_admin_mongo()
        
        print("Campo-SEriizable")
        # print(serializable)
        print("Campo-SEriizable")
        
        # for business in serializable["business"]:
        serializable["id"] = str(uuid.uuid4())
        serializable["date"] = datetime.now()
        
        # serializable["id"] = str(uuid.uuid5(uuid.NAMESPACE_DNS,"email"))
        serializable["date"] = datetime.now()

        print(collection.find_one({"id": str(idAdmin)}))
        print(str(idAdmin))

        collection.update_one(
            {"id":str(idAdmin)},
            {
                "$push":{
                    "business":serializable
                    
                }
            }
        )

        # collection.insert_one(serializable)
        

        conexion.close()
    
    @classmethod
    def get_list_business_id(self,idAdmin:str):
        try:
            collection, conexion = BDConnection.conexion_admin_mongo() 
            doc = collection.find_one(
                {"id": idAdmin},
                {"_id": 0, "business": 1}
            )
            
            print(doc)
            
            list_business = doc.get("business", []) if doc else []
            print(list_business)
                        
            # Convierte datetimes a str automáticamente
            doc_str = json.loads(json.dumps(list_business, default=str))
            print(doc_str)
            
            print(doc_str)
            if doc_str is None:
                conexion.close()
                return {
                    "status": 404,
                    "error": "usuario no encontrado"
                }
            elif isinstance(doc_str, list) and len(doc_str) == 0:
                conexion.close()
                return {
                    "status": 201,
                    "message": "Sin negocios disponibles"
                }
            else:
                return doc_str

        except Exception as e:
            return {
                "Error": str(e),
            }
    
    @classmethod
    def get_business_id(self, idBusiness):
        try:
            collection, conexion = BDConnection.conexion_admin_mongo() 
            doc = collection.find_one({"idAdmin":id,},{"_id": 0})
            
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