from app.models import AdminUser, Business, TimeZone, MethodPayment, SocialMedia, Feedback, CoWorker,CatalogItem,ClientUser,FollowBusiness,Cart,CartPayment,Products,Catalog,CatalogImage
from app.conexion import BDConnection
from datetime import datetime
from .serializers import  ClientUserSerializer,AdminUserSerializer
import json




class AdminContent():
    @classmethod
    def add_user(self, serializable:json):
        collection ,conexion= BDConnection.conexion_admin_mongo()
        
        print("Campo-SEriizable")
        print(serializable)
        print("Campo-SEriizable")
        
        #creacion modelo 
        # Datos del Admin
        user = AdminUser.objects.create(
            full_name=serializable["full_name"],
            first_name=serializable["first_name"],
            last_name=serializable["last_name"],
            dni=serializable["dni"],
            phone=serializable["phone"],
            country=serializable["country"],
            email=serializable["email"],
        )
        
        if "business" in serializable:
            for b in serializable.get("business"):
                print("business")
                
                business = Business.objects.create(
                    AdminUser=user,
                    idBot=b['idBot'],
                    name=b['name'],
                    category=b['category'],
                    ruc=b['ruc'],
                    phone_number=b['phone_number'],
                    phone_country_code=b['phone_country_code'],
                    catalog_url=b['catalog_url'],
                    description=b['description'],
                    address=b['address'],
                    logo_url=b['logo_url']
                )

                print(business)  # ✅ Ahora sí existe

                if "catalog" in b:
                    catalog = Catalog.objects.create(
                        business=business,
                    )

                    if "catalog_images" in b["catalog"]:
                        for catalog_image in b["catalog"]["catalog_images"]:
                            
                            catalog_im = CatalogImage.objects.create(
                                catalog=catalog,
                                name=catalog_image["name"],
                                type=catalog_image["type"],

                            )
                    if "catalog_items" in b["catalog"]:
                        for catalog_items in b["catalog"]["catalog_items"]:
                            catalog_it = CatalogItem.objects.create(
                                catalog=catalog,
                                name=catalog_image["name"],
                                description=catalog_image.get("description", ""),
                                    type=catalog_image["type"],
                                price=catalog_image["price"],
                                stock=catalog_image["stock"]
                            )


                if "method_payment" in b:
                    mp = b["method_payment"]
                    MethodPayment.objects.create(
                            business=business,
                            type=mp["type"],
                            name=mp["name"],
                            lastName=mp.get("lastName", ""),
                            email=mp.get("email", ""),
                            phone=mp.get("phone", ""),
                            phone_number=mp.get("phone_number", ""),
                            country_code=mp.get("country_code", ""),
                            qrImageUrl=mp.get("qrImageUrl", ""),
                            account_token=mp.get("account_token", ""),
                            public_key=mp.get("public_key", "")
                        )
                
                    print("social_media")

                if "social_media" in b:
                    for sm in b["social_media"]:
                        print(sm)
                        SocialMedia.objects.create(
                            business=business,
                            type_social=sm["type_social"],
                            urlPage=sm["urlPage"]
                        )

                if "co_workers" in b:
                    for cw in b["co_workers"]:
                        # cw = serializable["co_workers"] 
                        CoWorker.objects.create(
                            business=business,
                            coworker_id=cw.get("coworker_id", ""),
                            status=cw.get("status", "")
                        )

                if "feedback" in b:
                    
                    for  fb in b["feedback"]:
                    
                        Feedback.objects.create(
                            business=business,
                            name=fb["name"],
                            message=fb.get("message", "")
                        )

                if "time_zone" in b:
                        tz = b["time_zone"]
                        TimeZone.objects.create(
                            business = business,
                                time_open = tz["time_open"],
                                time_close = tz["time_close"]
                        )
            
        adminUserSerializer = AdminUserSerializer()
        json_data = adminUserSerializer.data

        collection.insert_one(json_data)
        

        conexion.close()

class ClientContent():
    @classmethod
    def add_user(self,serializable:json):
        collection, conexion = BDConnection.conexion_client_mongo()
        
        #creacion del modelo
        user = ClientUser.objects.create(
            # id = serializable["idClient"],
            full_name= serializable["full_name"],
            first_name = serializable["first_name"],
            last_name = serializable["last_name"],
            country = serializable["country"],
            email = serializable["email"],
            phone = serializable["phone"],
        )

        follow_business_list = []
        if "follow_business" in serializable and serializable["follow_business"]:
            for fb in serializable["follow_business"]:
               
                follow_business = FollowBusiness.objects.create(
                    clientUser=user,
                    id_conversation=fb["id_conversation"],
                    type=fb["type"]
                )
                
                print(follow_business)
                print(fb)
                print(fb.get("cart_payment"))
                
                if "cart_payment" in fb:
                    # print("true")
                    print()
                    print(fb.get("cart_payment")['cart_status'])
                    cartp = fb.get("cart_payment")
                    cart_payment = CartPayment.objects.create(
                        followBusiness = follow_business,
                        cart_status = cartp['cart_status'],    
                    )
                    
                    if "cart" in cartp:
                        carter = cartp.get("cart")
                        
                        cart = Cart.objects.create(
                            cartPayment = cart_payment,
                            total_price = carter['total_price']
                        )
                        
                        print("cart")
                        print(carter)
                        if "products" in carter:
                            for prod in carter.get("products"):
                                print("productos : --")
                                print(prod)
                                products = Products.objects.create(
                                    cart = cart,
                                    name = prod['name'],
                                    type = prod['type'],
                                    amount = int(prod['amount']),
                                    price = prod['price'],
                                )

                    
                #     print(cart_payment)
                    
            follow_business_list.append({
                "id_conversation": follow_business.id_conversation,
                "type": follow_business.type
            })
        else:
            
            print("No hay follow_business o está vacío.")
                            

        print(user)
        
        clientUserSerizable = ClientUserSerializer(user)
        json_data_client = clientUserSerizable.data
        
        print("User")
        print(clientUserSerizable)
        print(clientUserSerizable.data)
        print(serializable["follow_business"])
        
        

        collection.insert_one(json_data_client)
        conexion.close()


    @classmethod
    def search_user_email(email):
        collection, conexion    =BDConnection.conexion_client_mongo()
       
        user = collection.find_one({"email": email})
        
        conexion.close()
        return user
        
    @classmethod
    def search_id_client(id_client):
        collection, conexion    =BDConnection.conexion_client_mongo()
 
        user = collection.find_one({"idClientChatBot": id_client})
        
        conexion.close()
        return user
    
class FileContent():
    
    @classmethod
    def upload_logo_business(self,supabase,file,idAdmin:str):
        file_name= f"{idAdmin}/logo_business.jpg"
        file_content = file.read()
        
        try:
            response = supabase.storage.from_('administradores').upload(
                path=file_name,
                file=file_content,
            )
            return True
            
            
        except Exception as e:
            return {"error": str(e)}
    
    @classmethod
    def upload_image_catalog(self,supabase,file,idAdmin:str,index:int):
        file_name= f"{idAdmin}/catalog_business_{index}.jpg"
        file_content = file.read()
        
        try:
            response = supabase.storage.from_('administradores').upload(
                path=file_name,
                file=file_content,
            )
        except Exception as e:
            return {"error": str(e)}
        
        signed_url_data = supabase.storage.from_('admins').create_signed_url(file_name,3600)
        print(signed_url_data)
        
        return {
            "admin_id": idAdmin,
            "signed_url": signed_url_data["signedUrl"],  # ✅ FIX AQUÍ
            "filename": file_name
        }

    
    @classmethod
    def search_image_logo(self,supabase,idAdmin:str):
        try:
            file_name = f"{idAdmin}/logo_business.jpg"
            signed_url = supabase.storage.from_('administradores').create_signed_url(file_name, 3600)
            return signed_url
        except Exception as e:
            return {"error": str(e)}

    
