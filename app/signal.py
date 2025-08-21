from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
import uuid
from .models import Profile,UserType
from .models import User  # importa tu modelo real
from app.content.admin import AdminContent
from app.content.business import BusinessManager
from app.content.orders import OrdersManager
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
# from .thread_local import get_current_request
from datetime import datetime, timedelta

from app.views.stream import StreamOrder

from app.core.middleware import get_current_request
#crear usuario profile
@receiver(post_save, sender=User)
def crear_perfil_UserTest(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, type=UserType.CLIENTE)

# @receiver(pre_save, sender=Profile)
# def set_profile_id(sender, instance, **kwargs):
#     if not instance.id:
#         instance.id = str(uuid.uuid5(uuid.NAMESPACE_DNS, instance.email))


#precargar datos de usuario
@receiver(user_logged_in)
def set_session_user(sender, request, user, **kwargs):
    # print()
    responseAdmin = AdminContent.get_user_id(id=str(request.user.profile.id_profile  ))
    responseBusiness = BusinessManager.get_list_business_id(idAdmin=str(request.user.profile.id_profile))
    print(responseBusiness)
    request.session["user"] = responseAdmin
    request.session["business"]= responseBusiness
    print(request.session.get("user"))
    print(request.session.get("business"))
    print("señal ejecutada _precargar_")
    

@receiver(post_save, sender=Order)
def verificar_cantidad_ordenes(sender, instance,created, **kwargs):
    total_ordenes = Order.objects.count()
    print("ejecutando_signal_orders")


    # if created:

        # Order.objects.create(
        #     id_business="c37af9ad-e84f-4ae3-9d08-f7cce490b48f",
        #     id_client="4f1c3e0b-bf42-4c68-87d7-f3f6e7a1f4a9",
        #     carts={
        #         "products": [
        #             {"name": "Pizza Grande", "quantity": 2, "price": 27.50},
        #         ],
        #         "notes": "Extra queso"
        #     },
        #     total_amount=55.00,
        #     date=date.today() - timedelta(days=1)  # ayer
        # )

        # Order.objects.create(
        #     id_business="c37af9ad-e84f-4ae3-9d08-f7cce490b48f",
        #     id_client="4f1c3e0b-bf42-4c68-87d7-f3f6e7a1f4a9",
        #     carts={
        #         "products": [
        #             {"name": "Pizza Mediana", "quantity": 1, "price": 20.00}
        #         ],
        #         "notes": "Sin sal"
        #     },
        #     total_amount=20.00,
        #     date=date.today() - timedelta(days=2)  # anteayer
        # )


        # if total_ordenes >= 20:
        # OrdersManager.upload_orders()

    

@receiver(post_save, sender=Order)
def update_session_on_create(sender, instance, created, **kwargs):
    if created:
        request = get_current_request()
        print("signal ejecuntandose")
        if request:
            print("ejectuandose")
            orders_count = Order.objects.count()
            request.session['orders_count'] = orders_count
            request.session.modified = True
        
            
            stream = StreamOrder()
            stream.notify_stream()
            

@receiver(post_delete, sender=Order)
def update_session_on_delete(sender, instance, **kwargs):
    request = get_current_request()
    if request:
        orders_count = Order.objects.count()
        request.session['orders_count'] = orders_count
        request.session.modified = True
        
    