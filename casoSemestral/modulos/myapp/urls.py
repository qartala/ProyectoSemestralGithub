from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('login/', views.iniciar_sesion,name="iniciar_sesion"),
    path('logup/',views.registrarse,name='registrarse'),
    path('logout/',views.cerrar_sesion,name='cerrar_sesion'),
    path('buscar/', views.buscar, name='buscar'),
]
