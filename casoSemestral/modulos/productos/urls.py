from django.urls import path
from . import views

urlpatterns = [
    path('', views.listarProd,name="listar"),
    path('agregar/', views.agregarProd,name="agregar"),
    path('editar/<int:id>',views.modificar,name='editar'),
    path('eliminar/<int:id>',views.eliminarProd,name='eliminar'),
    path('cerrar/',views.cerrarSesion,name='cerrar')
   
]
