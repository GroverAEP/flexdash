from django.contrib import admin
from django.urls import path
from app.views import views
from app.views.order import OrderCreateAPIView,OrderCanceledView,OrderDashBoardView,OrderGetList
from app.views.dashboard import DashboardInfoTimeRealDay
from app.views.payment import PaymentProcess , PaymentCancelled

from app.content.orders import OrdersManager

#separo la vista en 2 
from app.views.stream import OrdersStreamView, OrdersStreamSafeView,OrdersStreamTodayView

#Admin
#client
#Analitycs
#Business
#orders

urlpatterns = [
    #run method function 
    #Get
    path('get_post/', views.obtener_pots, name="post1"),
    
    #Post
    path('upload_logo_business/', views.upload_logo_business,name="post"),
    # path('insertar_document/', views.connection_mongo, name="enviar_Dato"),
    #path unicamente para administradores (PageWeb)
    path('add_admin/', views.reg_admin, name= "add_admin"), 
    path('add_business/',views.reg_business, name= "reg_business"),


    path('login_admin/', views.login_admin, name="login_admin"),
    
    path('get-csrf/', views.get_csrf_token, name='get_csrf_token'),

    
    
    #path unicacmenete para los clientes vista(Bot)
    path('add_client/', views.add_client, name= "add_user"),
    
    path('validation_user/', views.validate_client, name="validation_user"),
    #Administracion o paginas de pruebas
    
    path('index/', views.index, name='index'),
    # path('generar_imagen/', views.generate_image, name="generate_image")   
    
    
    #PROCESO PAGO VALIDADO
    
    path('validated/', PaymentProcess.as_view(),name="validated-payment"),
    
    path('cancelled/', PaymentCancelled.as_view(), name="cancelled-payment"),
    
    

    
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

    # path('test/webhook/', views.test_webhook, name= "test_webhook"),
    # path('create_ticket/',views.create_ticket_load, name="create_ticket_load" ),
    
    path('test/generate_ticket_html/',views.generate_ticket_html, name ="generate_ticket_html"),
    path("checkout_ticket_url/<str:id_business>/<str:id_boleta>/", views.checkout_ticket, name="checkout_ticket"),

    path("create_order/",OrderCreateAPIView.as_view(), name="create_order"),
    path("remove_order/",OrderCanceledView.as_view(), name="remove_order"),
    
    path("dashboard/orders/", OrderDashBoardView.as_view(),name="dashboard-orders"),


    #
    path("orders/count/", OrderGetList.as_view(), name="orders_count"),

    path("analytics/orders",DashboardInfoTimeRealDay.as_view(), name="orders_analytics" ),

    path("orders/stream/<uuid:business_id>/", OrdersStreamView.as_view(), name="orders_stream"),
    path("orders/stream_pending_safe/<uuid:business_id>/", OrdersStreamSafeView.as_view(), name="orders-pending-safe"),
    path("orders/stream_pending_today/<uuid:business_id>/", OrdersStreamTodayView.as_view(), name="orders-pending-today"),
    
    
    path("upload_orders/", views.upload_orders_view, name="upload_orders"),
    ]

