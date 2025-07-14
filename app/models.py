# from django.db import models

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

# class Client(models.Model):
#     client_id = models.CharField(max_length=100)
#     id_chatbot = models.CharField(max_length=100, blank=True)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(blank=True)
#     phone = models.CharField(max_length=20, blank=True)
#     type_business = models.ManyToManyField(TypeBusiness)
#     date = models.DateField()

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"



# ####################################################


# # Redes sociales
# class SocialMedia(models.Model):
#     type_social = models.CharField(max_length=50)
#     url_page = models.URLField()

#     def __str__(self):
#         return f"{self.type_social} - {self.url_page}"

# # Métodos de pago
# class MethodPayment(models.Model):
#     PAYMENT_TYPES = [
#         ('yape', 'Yape'),
#         ('mercado_pago', 'Mercado Pago'),
#     ]

#     type = models.CharField(max_length=30, choices=PAYMENT_TYPES)
#     name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=20, blank=True)
#     qr_image_url = models.URLField(blank=True)

#     # Campos específicos de Mercado Pago
#     last_name = models.CharField(max_length=100, blank=True)
#     email = models.EmailField(blank=True)
#     phone_number = models.CharField(max_length=20, blank=True)
#     account_token = models.CharField(max_length=100, blank=True)
#     public_key = models.CharField(max_length=100, blank=True)

#     def __str__(self):
#         return self.type

# # Elemento del catálogo
# class CatalogItem(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     type = models.CharField(max_length=30)  # prod - serv
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.PositiveIntegerField()

#     def __str__(self):
#         return self.name

# # Co-trabajadores
# class CoWorker(models.Model):
#     coworker_id = models.CharField(max_length=100)
#     status = models.CharField(max_length=50)

#     def __str__(self):
#         return self.coworker_id

# # Negocio
# class Business(models.Model):
#     id_bot = models.CharField(max_length=100, blank=True)
#     name = models.CharField(max_length=100)
#     category = models.CharField(max_length=100)
#     ruc = models.CharField(max_length=20)
#     catalog_url = models.URLField()
#     description = models.TextField()
#     address = models.CharField(max_length=255)
#     time_open = models.TimeField()
#     time_close = models.TimeField()
#     logo_url = models.URLField()
#     feedback = models.TextField(blank=True)

#     catalog = models.ManyToManyField(CatalogItem)
#     co_workers = models.ManyToManyField(CoWorker)
#     method_payments = models.ManyToManyField(MethodPayment)
#     social_media = models.ManyToManyField(SocialMedia)

#     def __str__(self):
#         return self.name

# # Admin principal
# class Admin(models.Model):
#     full_name = models.CharField(max_length=150)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     dni = models.CharField(max_length=20)
#     phone = models.CharField(max_length=20)
#     email = models.EmailField()
#     business = models.ManyToManyField(Business)
#     date = models.DateField()

#     def __str__(self):
#         return self.full_name