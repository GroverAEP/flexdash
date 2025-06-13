from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('get_post/', views.obtener_pots, name="post1"),
    path('recibir_data/', views.recibir_dato,name="post"),
    path('insertar_document/', views.connection_mongo, name="enviar_Dato"),
    path('add_user/', views.add_user, name= "add_user")
]
