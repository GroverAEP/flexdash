from app.content.admin import AdminContent
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login


class AuthContent():
        
    @classmethod
    def reg_admin(cls, data):
        try:
            auth = data.get('auth', {})
        except Exception:
            return JsonResponse({
                "error": "claves de autenticación no creadas"
            }, status=400)
        
        username = data.get('username', None)
        email = data.get('email', None)
        password = auth.get('password', None)
        
   

        if not email or not password:
            return JsonResponse({'error': 'Email y password son obligatorios'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'El usuario ya existe'}, status=400)

        if not auth:
            return JsonResponse({'error': 'Claves de autenticación no existentes'}, status=404)

        # Crear usuario
        user = User.objects.create_user(username=username or email, email=email, password=password)
        print(user.profile.id_profile)

        # Agregar id_profile al data
        data["id"] = str(user.profile.id_profile)

        # Añadir usuario al grupo "admin"
        group, created = Group.objects.get_or_create(name="admin")
        user.groups.add(group)

        try:
            response, serializable = AdminContent.add_user(data)
            if response is None:
                # Si falla, eliminar usuario creado para no dejar datos inconsistentes
                user.delete()
                return JsonResponse({'error': 'Error al crear admin en contenido'}, status=500)
        except Exception as e:
            # Si ocurre cualquier excepción, eliminar usuario y devolver error
            user.delete()
            return JsonResponse({'error': f'Excepción: {str(e)}'}, status=500)

                    # data.pop("_id", None)  # Elimina si existe, si no, no hace nada

        serializable.pop("_id",None)
        print(serializable)
        return JsonResponse({
            "status": 200,
            "idObject": str(response),
            "response": serializable,
            "id_admin": user.profile.id_profile
        })
        
    
    @classmethod
    def login_admin(self,request,data):
        
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:  # Verifica si es admin o parte del staff
                login(request, user)
                return {"success": True, "message": "Admin login successful"}
            else:
                return {"success": False, "message": "User is not an admin"}
        else:
            return {"success": False, "message": "Invalid credentials"}