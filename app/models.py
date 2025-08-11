from django.db import models
from datetime import datetime
from django.utils import timezone

# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     type = models.CharField(max_length=50)  # ej: "prod", "serv"
#     amount = models.IntegerField()

#     def __str__(self):
#         return self.name

# class History(models.Model):
#     type_action = models.CharField(max_length=100)  # ej: "payment - processing - request"
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateField()
#     products = models.ManyToManyField(Product)

#     def __str__(self):
#         return f"{self.type_action} - {self.date}"

# class TypeBusiness(models.Model):
#     business_id = models.CharField(max_length=100)
#     history = models.ManyToManyField(History)

#     def __str__(self):
#         return self.business_id

# class ClientUser(models.Model):
#     id = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(blank=True)
#     phone = models.CharField(max_length=20, blank=True)
#     type_business = models.ManyToManyField(TypeBusiness)
#     date = models.DateField()
#     id_chatbot = models.CharField(max_length=100, blank=True)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"



# ####################################################


from django.db import models
import uuid


class ClientUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20,blank=True)
    country = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.full_name}"
class FollowBusiness(models.Model):
    class UserType(models.TextChoices):
        PAYMENT = 'payment', 'Payment'
        VISITOR = 'visitor', 'Visitor'
        BUYER = 'buyer', 'Buyer'
        FREQUENT = 'frequent_buyer', 'Frequent Buyer'
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    id_conversation =models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=UserType.choices,default=UserType.VISITOR)
    clientUser = models.ForeignKey(ClientUser,related_name="follow_business",on_delete=models.CASCADE)

class CartPayment(models.Model):
    class CartStatus(models.TextChoices):
        NEW = 'new', 'Empty Cart'
        PENDING = 'pending', 'Pending Purchase'

    followBusiness = models.OneToOneField(FollowBusiness, on_delete=models.CASCADE, related_name='cart_payment')
    cart_status = models.CharField(max_length=20, choices=CartStatus.choices, default=CartStatus.NEW)
    
class Cart(models.Model):
    cartPayment= models.OneToOneField(CartPayment, on_delete=models.CASCADE,related_name="cart")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)


    
    def __str__(self):
        return f"{self.CartPayment} - {self.date}"
    
    
class Products(models.Model):
    class ProductsType(models.TextChoices):
        SERV = 'serv','Servicios'
        PROD = 'prod','Productos'
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='products')
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20,choices=ProductsType.choices)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    
    
    

#########################################################
class AdminUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dni = models.CharField(max_length=15)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    email = models.EmailField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name


class Business(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    AdminUser = models.ForeignKey(AdminUser, related_name='business', on_delete=models.CASCADE)
    idBot = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    ruc = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20)
    phone_country_code = models.CharField(max_length=5, default="+51")
    catalog_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    logo_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Catalog(models.Model):
    business = models.OneToOneField(Business, related_name="catalog", on_delete=models.CASCADE)
    # catalog_image = CatalogImage(Business, related_name = 'catalog', on_delete=models.CASCADE)
    # catalog_items = CatalogItem()

class CatalogImage(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    catalog = models.ForeignKey(Catalog, related_name="catalog_images", on_delete= models.CASCADE)
    name = models.CharField(max_length=100,)
    type = models.CharField(max_length=100)
    img_url = models.URLField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    


class CatalogItem(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    catalog = models.ForeignKey(Catalog, related_name="catalog_items",on_delete= models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=50)  # "prod - serv"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class TimeZone(models.Model):
    business = models.OneToOneField(Business, related_name="time_zone", on_delete= models.CASCADE)
    time_open = models.TimeField()
    time_close = models.TimeField()
class CoWorker(models.Model):
    business = models.ForeignKey(Business, related_name='co_workers', on_delete=models.CASCADE)
    coworker_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, blank=True)


class Feedback(models.Model):
    business = models.ForeignKey(Business, related_name='feedback', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    message = models.TextField(blank=True)


class MethodPayment(models.Model):
    business = models.ForeignKey(Business, related_name='method_payments', on_delete=models.CASCADE)
    type = models.CharField(max_length=50)  # yape, mercado_pago, etc.
    name = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    country_code = models.CharField(max_length=10, blank=True)
    qrImageUrl = models.URLField(blank=True)
    account_token = models.CharField(max_length=255, blank=True)
    public_key = models.CharField(max_length=255, blank=True)


class SocialMedia(models.Model):
    business = models.ForeignKey(Business, related_name='social_media', on_delete=models.CASCADE)
    type_social = models.CharField(max_length=50)
    urlPage = models.URLField(blank=True, null=True, verbose_name="Página web")

#####################################################
#Profile
from django.contrib.auth.models import User
class UserType(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    CLIENTE = 'client', 'Client'
    SOPORTE = 'soport', 'Soport'



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_profile = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )# email = models.EmailField(blank=True, null=False)
    type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.CLIENTE)
    
    # phone = models.CharField(max_length=20,blank=True)
    is_active = models.BooleanField(default=True)   # ← Aquí está
    date = models.DateTimeField(auto_now_add=True)

    # avatar_url = models.URLField(blank=True, null=True)
    # def save(self, *args, **kwargs):
    #         if not self.id:
    #             # Genera UUID basado en el email
    #             self.id = str(uuid.uuid5(uuid.NAMESPACE_DNS, self.email))
    #         super().save(*args, **kwargs)

    def __str__(self):
            return f'Perfil de {self.user.username}'
        
    def get_id(self):
        return self.id_profile




class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CANCELLED = 'cancelled'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    id_business = models.UUIDField(default=uuid.uuid4,null=False, blank=False,editable=True	)
    id_client = models.UUIDField(default=uuid.uuid4,null=False, blank=False,editable=True	)  
    carts = models.JSONField(default=dict, blank=True)  # Datos adicionales de la orden
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.id} - {self.status}"