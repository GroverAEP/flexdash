from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
import uuid
from .models import Profile,UserType
from .models import User  # importa tu modelo real
from app.content.admin import AdminContent
from app.content.business import BusinessContent
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

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
    responseBusiness = BusinessContent.get_list_business_id(idAdmin=str(request.user.profile.id_profile))
    print(responseBusiness)
    request.session["user"] = responseAdmin
    request.session["business"]= responseBusiness
    print(request.session.get("user"))
    print(request.session.get("business"))
    print("señal ejecutada _precargar_")
    
    

@receiver(post_save, sender=Order)
def update_session_on_create(sender, instance, created, **kwargs):
    """
    Si se crea una orden, actualiza la sesión.
    """
    if created and hasattr(instance, '_request'):
        request = instance._request
        orders_count = Order.objects.count()
        request.session['orders_count'] = orders_count
        request.session.modified = True

@receiver(post_delete, sender=Order)
def update_session_on_delete(sender, instance, **kwargs):
    """
    Si se elimina una orden, actualiza la sesión.
    """
    if hasattr(instance, '_request'):
        request = instance._request
        orders_count = Order.objects.count()
        request.session['orders_count'] = orders_count
        request.session.modified = True