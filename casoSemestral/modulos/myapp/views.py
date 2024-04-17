from django.shortcuts import render,redirect ,get_object_or_404
from django.contrib.auth.models import User 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from modulos.productos.models import Producto
# Create your views here.

def index(request):
    productos = Producto.objects.all()
    datos = {
        'productos':productos
    }
    return render(request,'index.html',datos)


def registrarse(request):
    if request.method == 'GET':

        return render(request,'login/registrarse.html')
    
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                usuario= User.objects.create_user(username= request.POST['username'], password= request.POST['password1'],email=request.POST['email'])
                usuario.save()

                return redirect('iniciar_sesion')

            except:
                datos = {
                    'error':"El usuario ya existe"
                }
                return render(request,'login/registrarse.html',datos)
        
        else:
            
            datos = {
                'error': "Las contraseñas deben ser las mismas"
            }

            return render(request,'login/registrarse.html',datos)



def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'login/iniciar_sesion.html')
    
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])

        if user is None :
            #No se encontro al usuario
            datos = {
                "error":'No se encontro al usuario'
            }

            return render(request,'login/iniciar_sesion.html',datos)
        
        else:
            login(request,user)
            return redirect('index')
        


def cerrar_sesion(request):
    logout(request)
    return redirect('index')