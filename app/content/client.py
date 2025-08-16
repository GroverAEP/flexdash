from app.conexion import BDConnection

class ClientManager():
    
    def __init__(self,id_client):
        self.id_client = id_client
    
    
    def get_client_id(self):
        collection, conexion = BDConnection.conexion_client_mongo()
        
        client = collection.find_one({"id": self.id_client})
        
        if client:
            #determino que datos me va adevolver, solamente,
            response = {
               "first_name" : client["first_name"],
                "last_name" : client["last_name"],
                "phone" : client["phone"],
                "email" : client["email"]
            }
            
            
            return response
        