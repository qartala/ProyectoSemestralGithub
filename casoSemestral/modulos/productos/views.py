from django.shortcuts import render,redirect,get_object_or_404 
from modulos.productos.forms import compraForm, productoForm
from modulos.productos.models import Favorito, Producto,Carrito, OrdenCompra,compraProducto, comunas_santiago
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect ,HttpResponse
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import sweetify
from django.core.paginator import Paginator
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import os
from django.conf import settings
from .models import OrdenCompra, compraProducto, Producto, Carrito, User ,comunas_santiago


# Create your views here.

@login_required
def listarProd(request):
    productos = Producto.objects.all()
    paginator = Paginator(productos, 10)  # Divide los productos en páginas de 6 elementos cada una
    page_number = request.GET.get('page')  # Obtiene el número de página actual desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página actual

    datos = {
        'page_obj': page_obj
    }
    return render(request, 'productos/listar.html', datos)



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

        usuario = request.user
        es_favorito = Favorito.objects.filter(usuario=usuario, producto=producto).exists()
        datos = {
            'producto': producto,
            'favorito':es_favorito
        }

        return render(request, 'productos/detalleProd.html',datos)
    else:
        pass

def agregar_favorito(request, id):
    usuario = request.user
    producto = Producto.objects.get(pk=id)

    Favorito.objects.create(usuario=usuario, producto=producto)

    return redirect(reverse('detalle', kwargs={'id': id}))

@login_required
def quitar_favorito(request, id):
    usuario = request.user
    producto = Producto.objects.get(pk=id)


    favorito = Favorito.objects.filter(usuario=usuario, producto=producto)

    favorito.delete()
    return redirect(reverse('detalle', kwargs={'id': id}))



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
        sweetify.success(request, 'Producto añadido al carrito', icon='success', persistent='Aceptar')


    except Exception:
        #No hay carrito para el producto
        carrito= Carrito()
        carrito.cantidad = 1 
        carrito.subtotal = producto.precio
        carrito.producto = producto
        carrito.usuario = usuario
        carrito.save()
        sweetify.success(request, 'Producto añadido al carrito', icon='success', persistent='Aceptar')

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



# def orden_compra(request, total):
#     if request.method == 'GET':
#         valor_total = total
#         datos = {
#             'total': valor_total,
#             'comunas':comunas_santiago
#         }

#         return render(request,'compra/ordencompra.html',datos)
    
#     if request.method=='POST':
#             try:
#                 carritos = Carrito.objects.filter(usuario = request.user.id)
#                 usuario = User.objects.get(id = request.user.id)
                
#                 direccion = request.POST['direccion']
#                 recibe = request.POST['recibe']
#                 comuna = request.POST['comuna']

#                 orden = OrdenCompra()
#                 orden.total = total
#                 orden.direccion = direccion
#                 orden.recibe = recibe
#                 orden.comuna = comuna 
#                 orden.usuario = usuario
#                 orden.save()

#                 for producto in carritos :
#                     compra = compraProducto()
#                     compra.cantidad = producto.cantidad
#                     compra.subtotal = producto.subtotal
#                     compra.nombre = producto.producto.nombre
#                     compra.compra = orden

#                     producto_enc = Producto.objects.get(id = producto.producto.id)
#                     producto_enc.stock = producto_enc.stock - compra.cantidad

#                     producto_enc.save()
#                     compra.save()
                    
#                 carritos.delete()
#                 return redirect('index')
            

#             except:
#                 datos = {
#                     'error':'Ha ocurrido un error inesperado'
#                     }
#                 return render(request,'compra/orden')

def generar_pdf(filepath, orden):
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Encabezado
    elements.append(Paragraph('Orden de Compra', styles['Title']))
    elements.append(Paragraph(f'Dirección: {orden.direccion}', styles['Normal']))
    elements.append(Paragraph(f'Comuna: {orden.comuna}', styles['Normal']))
    elements.append(Paragraph(f'Recibe: {orden.recibe}', styles['Normal']))
    elements.append(Paragraph(f'Usuario: {orden.usuario}', styles['Normal']))

    elements.append(Spacer(1, 12))

    # Tabla de productos
    data = [['Producto', 'Cantidad', 'Subtotal']]
    productos = compraProducto.objects.filter(compra=orden)
    for producto in productos:
        data.append([producto.nombre, producto.cantidad, f'${producto.subtotal}'])

    # Estilo de la tabla
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    elements.append(Spacer(1, 12))

    # Total
    elements.append(Paragraph(f'Total: ${orden.total}', styles['Normal']))

    # Construir PDF
    doc.build(elements)



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
                
                pdf_filename = f"orden_compra_{orden.id}.pdf"
                pdf_filepath = os.path.join(settings.MEDIA_ROOT, pdf_filename)
                generar_pdf(pdf_filepath, orden)

                # Eliminar los productos del carrito
                carritos.delete()

                # Redirigir al usuario a una página donde pueda descargar el PDF
                return redirect('descargar_pdf', filename=pdf_filename)

            except:
                datos = {
                    'error':'Ha ocurrido un error inesperado'
                    }
                return render(request,'compra/ordencompra.html')




def descargar_pdf(request, filename):
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(filepath):
        with open(filepath, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponse("El archivo no existe.")     


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



@login_required
def favoritos(request):
    favoritos = Favorito.objects.filter(usuario=request.user)
    productos_favoritos = Producto.objects.filter(id__in=[favorito.producto_id for favorito in favoritos])
    return render(request, 'productos/favoritos.html', {'productos_favoritos': productos_favoritos})


@login_required
def envioProductos(request):
    orden = OrdenCompra.objects.all()
    compraUsuario = compraProducto.objects.filter(compra__in = orden)

    datos = {
        "compraUsuario" : compraUsuario,
        "orden": orden

    }

    return render(request,'compra/EnvioProductos.html',datos)

@login_required
def estadoCompra(request, id):
    if request.method == 'GET':
        orden = get_object_or_404(OrdenCompra, id=id)
        datos = {
            "formulario": compraForm(instance=orden)
        }
        return render(request, 'compra/estadoCompra.html', datos)

    else:
         
        try:
            orden = get_object_or_404(OrdenCompra, id=id)
            ord_act = compraForm(request.POST, instance=orden)
            ord_act.save()
            return redirect('enviocompra')
        except:
            
            datos ={
                'error':'Ha ocurrido un error inesperado',
                'formulario':compraForm(instance= get_object_or_404(OrdenCompra, id = id))
            }
            return render(request,'compra/estadoCompra.html', datos)


