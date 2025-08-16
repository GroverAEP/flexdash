from app.conexion import BDConnection
from datetime import datetime

class CustomersManagers():
   
   def __init__(self,id_business):
    self.id_business = id_business
    
    def add_customers():

        pass
    def vef_customers(self,id_client):
        collection, conexion =BDConnection.conexion_business_mongo()
        business = collection.find_one({"id": id_business})
        # customers = business["customers"]
        
        # if client in customers:
        #     client["id"] == id_client 
        if not business:
            conexion.close()
            return False, "Negocio no encontrado"

        # Verificar si existe la lista customers
        if "customers" in business:
            for client in business["customers"]:
                if client["id_client"] == id_client:
                    client["type"] == "currently"
                    conexion.close()
                    return False, "Cliente ya existe"
                    
            
        # sino existe que agre al customers, los datos de data
        data = {
            "id_client": id_client,
            "type": "new",
            "date": datetime.now()
        }
        
        # Agregar cliente
        business["customers"].append(data)

        # Guardar cambios
        collection.update_one(
            {"id": id_business},
            {"$set": {"customers": business["customers"]}}
        )

        conexion.close()
        return True, "Cliente agregado correctamente"
        
    def get_customer(self,id_client):
        pass
    
    def remove_customers():
        pass

class AnalyticsCustomers:

    
    def blocked_phone_5_for_business_cancelled():
        pass