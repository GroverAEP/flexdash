from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from app.auth import AuthContent


from django.middleware.csrf import get_token

from django.http import JsonResponse,HttpResponse

from django.contrib.auth import logout
from django.contrib.auth.models import User

# from django.shortcuts import render
# Create your views here.
from django.views.decorators.csrf import csrf_protect
from app.content.admin import AdminContent



import json


route_auth = "auth/"
route_account = "account/"
route_options = "options/"
route_business= "business/"

#test

def incrementar_contador(request):
    if request.method == "POST":
        contador = request.session.get("contador", 0) + 1
        request.session["contador"] = contador
        return JsonResponse({"contador": contador})
    return JsonResponse({"error": "Método no permitido"}, status=405)


#registro

def accountAuth(request):
    
    return render(request, f"{route_account}auth.html")

@csrf_protect
def accountLogin(request):
    if request.method == "POST":
        # form = UserCreationForm(request.POST)
        # print(form)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            
            login(request,user)
            messages.success(request, "Inicio de sesion exitoso")
            return redirect("account-dashboard")
        else:
            messages.error(request,"Usuario o contraseña incorrectos")
    elif request.method != "GET":
        return render("<div>No ventana no existinte</div>")
    else:
       auth = AuthContent.vef_auth_session(user=request.user)
    #    print(response)
       if auth:
            # response = AdminContent.get_user_id(id=request.user.profile.id_profile)
            
            # request.session['user'] = response
            return auth
            
    return render(request,f"{route_auth}login.html")


#Desccartar el registro de esta manera // No es necesario aun.
#Por que solamente crea el usuario , No crea los datos en la bd
# def accountRegister(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         print(form)
#         if form.is_valid():
#             user = form.save()
#             login(request,user)
#             get_token(request)            
#             messages.success(request,"Registro exitoso, Bienvenido")
#             AuthContent.reg_user_admin()
#             return redirect("account-dashboard")
#         else:
#             messages.error(request, "Porfavor, verifica los errores")
#             # return render(request,f"{route_auth}auth.html")
#     elif request.method != "GET":
#         return render("<div>No ventana no existinte</div>")
#     else:

#             form = UserCreationForm()
#             response = AuthContent.vef_auth_session(user=request.user)
        
#             print(response)
#             if response:
#                 return response
            
        
            
#     return render(request, f"{route_auth}register.html", {"form": form})
#     # return render(request,f"{route_account}auth.html")
    




# Visual


from django.contrib.auth.models import AnonymousUser



# @login_required
def accountDashboard(request):
    if request.method != "GET":
        return JsonResponse({"error": "metodo no permitido"},)
    
    # if request.user Ano:
    #     print(request.user)
    #     return JsonResponse({"error": "usuario no logueado"})
    
    # print(request.user.profile.id_profile)
    # print(request.session.get('user'))
    # print(request.session.get)
    # if request.session.get('user') is None:
    #     response = AdminContent.get_user_id(id=request.user.profile.id_profile)
    #     request.session['user'] = response
        # data = json.loads(request.body)
        
    
    
    return render(request, f"{route_account}dashboard.html")


def accountBusiness(request):
    if request.method == "GET":
        # data = json.loads(request.body)
    
        return render(request, f"{route_account}business.html")


def options(request):
    if request.method == "GET":
        
        return render(request,f"{route_business}options.html")

def optionPassword_reset(request):
    return render(request,f"{route_options}password_reset.html")

def optionLogout(request):
   
    logout(request)
    return redirect('login')  # Cambia 'login' por el nombre de tu URL para el login

    # if request.method == "GET":
    # data = json.loads(request.body)
    return render(request, F"{route_options}/logout.html")





#Business
# def selectedBusiness(request):
#     list_business = request.session["user"]["business"]
    
#     for business in list_business:
#         request.session["business"] = business
#     redirect()


def accountBusinessDashboard(request):
    # if request.method == "POST":
    #     print("metodo post para utilizar")
    #     business_id = request.POST.get("business_id")
    #     # request.session["select"]
  
    #     # return JsonResponse({"OpenBusiness"})    
    
    #     # Aquí puedes procesar business_id, por ejemplo:
        
    #     list_business = request.session.get('business', [])
        
        
        
    #     # Buscar negocio por id
    #     negocio = next((b for b in list_business if str(b.get('id')) == str(business_id)), None)
    #     request.session["unique_business"] = negocio
        
    #     if negocio:
    #          # Lógica para generar evento con business_id
    #          return render(request,f"{route_business}dashboard.html",)
    #     else:
    #         return JsonResponse({"error": "No se envió business_id"})
    
        
    return render(request, f"{route_business}dashboard.html")
    # return JsonResponse({"ERROR":"metodo invalido" + request.method})
    
    
    
    

def accountBusinessPreorders(request):
    # request.session.business
    
    
    return render(request,f"{route_business}pre_orders.html")