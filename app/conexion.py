from pymongo import MongoClient 
from pymongo.mongo_client import MongoClient
from django.conf import settings
from pymongo.server_api import ServerApi
import certifi
import os
class BDConnection:
    @staticmethod
    def connection_mongo():
        client = MongoClient(
            os.environ.get("MONGO_ATLAS_KEY"),
            # settings.MONGO_ATLAS_KEY,
            server_api=ServerApi('1'),
            tlsCAFile=certifi.where(),
            uuidRepresentation='standard'
        )
        print(f"Conexión exitosa con {client}")
        return client

    @classmethod
    def conexion_client_mongo(cls):
        conexion = cls.connection_mongo()
        collection = conexion['vlexWay']
        return collection['clients'], conexion  # devuelve también la conexión para cerrar luego

    @classmethod
    def conexion_admin_mongo(cls):
        conexion = cls.connection_mongo()
        collection = conexion['vlexWay']
        return collection['admins'], conexion
    
    @classmethod
    def conexion_order_mongo(cls):
        conexion = cls.connection_mongo()
        collection = conexion['vlexWay']
        return collection['orders'], conexion