from app.conexion import BDConnection
from django.http import JsonResponse
import json
from datetime import datetime
import uuid

class BusinessManager():
    @classmethod
    def reg_business(self,idAdmin,serializable):
        collection, conexion = BDConnection.conexion_business_mongo()
        
        #Colocando el id_admin: Enel serializable
        print(idAdmin)
        
        serializable["id_admin"] = str(idAdmin)
        
        #GENERO LA IDENTIFICACION UUID
        serializable["id"] = str(uuid.uuid4())
        #GENERO LA FECHA DE AHORA
        serializable["date"] = datetime.now().isoformat()

        # serializable["customers"]

        # print(collection.find_one({"id_admin": str(idAdmin)}))
        
        #VERIFICO SI EL NEGOCIO ESTA GENERADO CON ALGUN OTRO
        # if collection.find_one({"id_admin": str(idAdmin)}):
        
        print(serializable)
        # json_string = json.dumps(serializable)


        collection.insert_one(serializable) 
        
        conexion.close()
    
    
    # @classmethod
    # def reg_business(self,idAdmin,serializable):
    #     # def add_user(self, serializable:json):
    #     collection ,conexion= BDConnection.conexion_admin_mongo()
        
    #     print("Campo-SEriizable")
    #     # print(serializable)
    #     print("Campo-SEriizable")
        
    #     # for business in serializable["business"]:
    #     serializable["id"] = str(uuid.uuid4())
    #     serializable["date"] = datetime.now()
        
    #     # serializable["id"] = str(uuid.uuid5(uuid.NAMESPACE_DNS,"email"))
    #     serializable["date"] = datetime.now()

    #     print(collection.find_one({"id": str(idAdmin)}))
    #     print(str(idAdmin))

    #     collection.update_one(
    #         {"id":str(idAdmin)},
    #         {
    #             "$push":{
    #                 "business":serializable
                    
    #             }
    #         }
    #     )

    #     # collection.insert_one(serializable)
        

    #     conexion.close()
    
    @classmethod
    def get_list_business_id(self,idAdmin:str):
        try:
            collection, conexion = BDConnection.conexion_business_mongo() 
            list_business = collection.find(
                {"id_admin": idAdmin},
                {"_id": 0}
            )
            
            # print(doc)
            
            # list_business = doc.get("business", []) if doc else []
            print(list_business)
            # docs_list = list(docs)

            # Convierte datetimes a str automáticamente
            doc_str = json.loads(json.dumps(list(list_business), default=str))
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
            collection, conexion = BDConnection.conexion_business_mongo() 
            doc = collection.find_one({"id":idBusiness,},{"_id": 0})
            
            
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