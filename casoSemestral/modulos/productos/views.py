from django.shortcuts import render,redirect,get_object_or_404 
from modulos.productos.forms import productoForm
from modulos.productos.models import Producto,Carrito, OrdenCompra,compraProducto, comunas_santiago
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
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


@login_required
def detalleProd(request, id ):
    if request.method  == 'GET':
        producto  =get_object_or_404(Producto, id = id) 
        datos = {
            'producto': producto
        }

        return render(request, 'productos/detalleProd.html',datos)
    else:
        pass

@login_required
def añadirCarrito(request, id ):
    usuario = User.objects.get(id = request.user.id)
    producto = Producto.objects.get(id = id)
    
    
    try:
        #Ya hay carrito para el producto
        carrito = Carrito.objects.get(producto = id, usuario =request.user.id)
        carrito.cantidad = carrito.cantidad + 1 
        carrito.subtotal = (carrito.cantidad * producto.precio)
        carrito.save()

    except Exception:
        #No hay carrito para el producto
        carrito= Carrito()
        carrito.cantidad = 1 
        carrito.subtotal = producto.precio
        carrito.producto = producto
        carrito.usuario = usuario
        carrito.save()

    return redirect('index')

@login_required
def carro(request):
    carrito = Carrito.objects.filter(usuario = request.user.id)

    if carrito.exists():
        total = 0 
        for carro in carrito:
            total += carro.subtotal
                
        datos = {
                'carrito':carrito,
                'total':total
        }

        return render(request,'compra/carrito.html',datos)
    else:
        datos = {
            'mensaje':'Aun no tienes nada en el carrito'
        }
        return render(request,'compra/carrito.html',datos)
   
    
@login_required
def restarProd(request,id):
    carrito = Carrito.objects.get(producto = id, usuario = request.user.id)
    carrito.cantidad = carrito.cantidad - 1  
    carrito.subtotal = carrito.cantidad * carrito.producto.precio
    if carrito.cantidad == 0 :
        carrito.delete()
        return HttpResponseRedirect(reverse('carrito'))
    
    else:
        carrito.save()
        return HttpResponseRedirect(reverse('carrito'))

@login_required
def añadirProd(request, id):
    carrito = Carrito.objects.get(producto = id , usuario = request.user.id)
    carrito.cantidad = carrito.cantidad + 1 
    carrito.subtotal = carrito.cantidad * carrito.producto.precio
    carrito.save()
    return HttpResponseRedirect(reverse('carrito'))

@login_required
def eliminarCarro(request):
    carrito = Carrito.objects.filter(usuario = request.user.id)
    carrito.delete()
    return HttpResponseRedirect(reverse('carrito'))



def orden_compra(request, total):
    if request.method == 'GET':
        valor_total = total
        datos = {
            'total': valor_total,
            'comunas':comunas_santiago
        }

        return render(request,'compra/ordencompra.html',datos)
    
    if request.method=='POST':
            try:
                carritos = Carrito.objects.filter(usuario = request.user.id)
                usuario = User.objects.get(id = request.user.id)
                
                direccion = request.POST['direccion']
                recibe = request.POST['recibe']
                comuna = request.POST['comuna']

                orden = OrdenCompra()
                orden.total = total
                orden.direccion = direccion
                orden.recibe = recibe
                orden.comuna = comuna 
                orden.usuario = usuario
                orden.save()

                for producto in carritos :
                    compra = compraProducto()
                    compra.cantidad = producto.cantidad
                    compra.subtotal = producto.subtotal
                    compra.nombre = producto.producto.nombre
                    compra.compra = orden

                    producto_enc = Producto.objects.get(id = producto.producto.id)
                    producto_enc.stock = producto_enc.stock - compra.cantidad

                    producto_enc.save()
                    compra.save()
                    
                carritos.delete()
                return redirect('index')
            

            except:
                datos = {
                    'error':'Ha ocurrido un error inesperado'
                    }
                return render(request,'compra/orden')
        
def restarProductosBD(idProducto , cantidad):
    producto_encontrado = Producto.objects.get(id = idProducto)
    

    if producto_encontrado.stock < cantidad:
        cantidad = producto_encontrado.stock

    producto_encontrado.stock = producto_encontrado.stock- cantidad


@login_required
def listaOrdenes(request):
    
    ordenes = OrdenCompra.objects.filter(usuario = request.user.id)
    if ordenes.exists():
        compras =compraProducto.objects.filter(compra__in = ordenes)
        datos = {
            'ordenes':ordenes,
            'compras':compras
        }
        return render(request,'compra/listacompras.html',datos)
    else:
        datos = {
            'mensaje':'Aun no has realizado una compra'
        }
        return render(request, 'compra/listacompras.html',datos)

#Quitar cuando ya este todo listo
def eliminarLOl(request):
    ordenes = OrdenCompra.objects.filter(usuario = request.user.id)
    ordenes.delete()
    return redirect('index')
