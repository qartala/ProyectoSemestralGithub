from django.shortcuts import render,redirect,get_object_or_404
from modulos.productos.forms import productoForm
from modulos.productos.models import Producto
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import sweetify

# Create your views here.

@login_required
def listarProd(request):
    productos = Producto.objects.all()

    datos = {
        'productos':productos
    }
    return render(request,'productos/listar.html',datos)




@login_required
def agregarProd(request):
    if request.method == 'POST':
        print(request.POST)
        producto_form = productoForm(request.POST,request.FILES)
       
        if producto_form.is_valid() :
            producto = producto_form.save()
            producto.save()
            return redirect('listar')
        
        sweetify.success(request, title='Hecho', text = 'Producto guardado correctamente')
    else:
        producto_form = productoForm()

    return render(request, 'productos/agregar.html', {'producto_form': producto_form})

@login_required
def modificar(request,id):
    if request.method == 'GET':
       
        producto = get_object_or_404(Producto,id =id)
        datos = {
            'formulario':productoForm(instance= producto),
            'idprod':producto.id
        }

        return render(request,'productos/modificar.html',datos)
    
    else:
        try:

            producto = get_object_or_404(Producto,id =id)
            prod_act = productoForm(request.POST,request.FILES, instance=producto)
            prod_act.save()
            return redirect('listar')
        
        except:
            datos = {
                'error':'Ha ocurrido un error inesperado',
                'formulario':productoForm(instance=get_object_or_404(Producto,id =id))
            }

            return render(request,'productos/modificar.html',datos)
        
@login_required
def eliminarProd(request, id):
    producto  = get_object_or_404(Producto, id = id)
    producto.delete()

    return redirect('listar')


@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('index')