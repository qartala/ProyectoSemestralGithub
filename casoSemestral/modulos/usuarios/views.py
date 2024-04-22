from django.shortcuts import redirect, render
from django.contrib.auth.models import User


# Create your views here.
def registrarAdmin(request):
    if request.method == 'GET':
        return render(request,'login/registrarAdmin.html')
    
    else:
        if request.POST['contraseña1'] == request.POST['contraseña2']:
           
            try:
                usuario = User.objects.create_user(username=request.POST['usuario'],password=request.POST['contraseña1'],is_staff = True)
                usuario.save()
                return redirect('listar')

                
            except:

                datos = {
                    'error':'El usuario ya existe'
                }
                return render(request,'login/registrarAdmin.html',datos)



        else:
            datos = {
                'error':'Las contraseñas son distintas'
            }

            return render(request,'login/registrarAdmin.html',datos)
