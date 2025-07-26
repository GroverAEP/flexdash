# serializers.py

from rest_framework import serializers
from .models import ClientUser, FollowBusiness, CartPayment, Cart, Products         
from .models import Business, AdminUser,TimeZone,CoWorker,Feedback,MethodPayment,SocialMedia,CatalogImage,CatalogItem,Catalog


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = [
            'id',
            'type_social',
            'urlPage',
        ]



class MethodPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MethodPayment
        fields = [
            'id',
            'type',
            'name',
            'lastName',
            'email',
            'phone',
            'phone_number',
            'country_code',
            'qrImageUrl',
            'account_token',
            'public_key',
        ]



class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            'id',
            'name',
            'message',
        ]

class CoWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoWorker
        fields = [
            'id',
            'coworker_id',
            'status',
        ]
class CatalogItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogItem
        fields = ['id', 'name', 'description', 'type', 'price', 'stock', 'date']

class CatalogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogImage
        fields = ['id', 'name', 'type', 'img_url']

class CatalogSerializer(serializers.ModelSerializer):
    catalog_items = CatalogItemSerializer(many=True,required= False)
    catalog_images = CatalogImageSerializer(many=True,required = False)

    class Meta:
        model = Catalog
        fields = ['catalog_items', 'catalog_images']

class TimeZoneSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = TimeZone
        fields = [
            'time_open',
            'time_close',
        ]



class BusinessSerializer(serializers.ModelSerializer):
    social_media =   SocialMediaSerializer(many=True, required= False)
    method_payment = MethodPaymentSerializer(many=True, required= False)
    feedback = FeedbackSerializer(many=True, required= False)
    co_workers = CoWorkerSerializer(many=True, required= False)
    catalog = CatalogSerializer(required= False)
    time_zone = TimeZoneSerializer(required=False)
    
    class Meta:
        model = Business
        fields = [
            'id',
            'idBot',
            'name',
            'category',
            'ruc',
            'phone_number',
            'phone_country_code',
            'catalog_url',
            'description',
            'address',
            'logo_url',
            
            'method_payment',
            'social_media',
            'co_workers',
            'catalog',
            'feedback',
            'time_zone',

        ]


class AdminUserSerializer(serializers.ModelSerializer):
    
    business = BusinessSerializer(many=True, required=False)
    
    class Meta:
        model = AdminUser
        fields = [
            'id',
            'full_name',
            'first_name',
            'last_name',
            'dni',
            'phone',
            'country',
            'email',
            'date',
            'business',
        ]
##############################################

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'type', 'amount', 'price', 'date', 'cart']

class CartSerializer(serializers.ModelSerializer):
    products = ProductsSerializer(many=True,required = False)  # si hay relación inversa

    class Meta:
        model = Cart
        fields =  ['total_price', 'date', 'products']



class CartPaymentSerializer(serializers.ModelSerializer):
    cart = CartSerializer(required = False)
    class Meta:
        model = CartPayment
        fields = ['cart', 'cart_status']
        
        
class FollowBusinessSerializer(serializers.ModelSerializer):
    cart_payment = CartPaymentSerializer(required=False)  # <-- usa el related_name exacto
    
    class Meta:
        model = FollowBusiness
        fields = ['id_conversation', 'type','cart_payment']  # solo lo que quieres devolver


class ClientUserSerializer(serializers.ModelSerializer):
    # idClient = serializers.UUIDField(source='id', read_only=True)
    follow_business = FollowBusinessSerializer(many=True, required=False)

    class Meta:
        model = ClientUser
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'country', 'date', 'follow_business',
        ]







