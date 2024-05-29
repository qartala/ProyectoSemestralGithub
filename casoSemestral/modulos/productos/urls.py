from django.urls import path
from . import views

urlpatterns = [
    path('', views.listarProd,name="listar"),
    path('agregar/', views.agregarProd,name="agregar"),
    path('editar/<int:id>',views.modificar,name='editar'),
    path('eliminar/<int:id>',views.eliminarProd,name='eliminar'),
    path('cerrar/',views.cerrarSesion,name='cerrar'),
    path('detalle/<int:id>', views.detalleProd, name='detalle'),
    path('añadir/<int:id>',views.añadirCarrito, name='añadir'),
    path('carrito/',views.carro, name='carrito'),
    path('restar/<int:id>',views.restarProd, name= 'restar'),
    path('sumar/<int:id>',views.añadirProd,name='sumar'),
    path('vaciar',views.eliminarCarro,name='vaciar'),
    path('ordencompra/<int:total>',views.orden_compra,name='ordencompra'),
    path('listacompras',views.listaOrdenes,name='listaCompras'),
    path('omega',views.eliminarLOl,name='omega'),
    path('guardar_favorito/<int:id>',views.agregar_favorito,name='guardarFavorito'),
    path('quitar_favorito/<int:id>',views.quitar_favorito,name="quitar_fav")
   
]
