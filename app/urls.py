from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    #run method function 
    #Get
    path('get_post/', views.obtener_pots, name="post1"),
    
    #Post
    path('upload_image_to_supabase/', views.upload_image_to_supabase,name="post"),
    # path('insertar_document/', views.connection_mongo, name="enviar_Dato"),
    path('add_user/', views.add_user, name= "add_user"),
    path('add_admin/', views.add_admin, name= "add_admin"), 
    path('validation_user/', views.validation_user, name="validation_user"),
    #Administracion o paginas de pruebas
    
    path('index/', views.index, name='index'),
    # path('generar_imagen/', views.generate_image, name="generate_image")   
    
    

    
    #Test
    
    path('get_error/', views.get_error, name="get_error"),
    path('post_json_test', views.obtener_post_pagina, name="postTest"),
    path('get_json_test', views.get_json_test, name="get_json_test" ),
    
    path('subir_catalogo/',views.subir_catalogo_admin, name="subir_catalogo"),
    
    path('cal_price_total/',views.cal_price_total, name="cal_price_total"),
    #Test Mercado Pago
    path('test_pago_yape_mercadopago',views.crear_pago, name="test_pago"),

    

    #payment_methods
    path('payment-methods/', views.payment_methods, name='payment_methods'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failure/', views.payment_failure, name='payment_failure'),
    path('payment-pending/', views.payment_pending, name='payment_pending'),
    path('webhook/', views.payment_webhook, name='payment_webhook'),
    path('payment-status/<str:order_id>/', views.payment_status, name='payment_status'),

    path('create_yape_payment/', views.create_yape_payment, name= "create_yape_pay"),
    path('api/payment_notifications/', views.payment_notifications,name="payment_notifications"),

    path('test/webhook/', views.test_webhook, name= "test_webhook")

]

