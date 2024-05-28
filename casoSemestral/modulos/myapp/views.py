from django.shortcuts import render,redirect ,get_object_or_404
from django.contrib.auth.models import User 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from modulos.productos.models import Producto
from django.core.paginator import Paginator
import sweetify 


# Create your views here.

# def index(request):
#     productos = Producto.objects.all()
#     datos = {
#         'productos':productos
#     }
#     return render(request,'index.html',datos)

def index(request):
    productos = Producto.objects.all()
    paginator = Paginator(productos, 6)  # Divide los productos en páginas de 6 elementos cada una
    page_number = request.GET.get('page')  # Obtiene el número de página actual desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página actual

    datos = {
        'page_obj': page_obj
    }
    return render(request, 'index.html', datos)



def registrarse(request):
    if request.method == 'GET':

        return render(request,'login/registrarse.html')
    
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                usuario= User.objects.create_user(username= request.POST['username'], password= request.POST['password1'],email=request.POST['email'])
                
                if usuario.username == 'admin':
                    usuario.is_staff = True

                usuario.save()

                return redirect('iniciar_sesion')

            except: 
                
                datos = {
                    'error':"El usuario ya existe"
                }
                sweetify.warning(request, title='Error',text = 'El usuario ya existe', persistent= 'Confirmar')

                return render(request,'login/registrarse.html',datos)
        
        else:
            
            datos = {
                'error': "Las contraseñas deben ser las mismas"
            }
            sweetify.warning(request, title = 'Error: Contraseña', text= 'Las contraseñas son diferentes', persistent= 'Confirmar')

            return render(request,'login/registrarse.html',datos)



def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'login/iniciar_sesion.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            # No se encontró al usuario
            sweetify.warning(request, title= 'Error: Usuario y contraseña', text ='Verifique el usuario y contraseña')
            datos = {
                "error": 'No se encontró al usuario'
            }
            return render(request, 'login/iniciar_sesion.html', datos)
        else:
            login(request, user)
            if user.is_staff == True :
                return redirect('listar')

            else:
                return redirect('index')
        

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('index')