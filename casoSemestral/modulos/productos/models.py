from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

# Create your models here.
categorias = [
        ('Electronicos', 'Electronicos'),
        ('Notebooks', 'Notebooks'),
        ('Celulares', 'Celulares'),
        ('Consolas', 'Consolas'),
        ('Tablets', 'Tablets'),
        ('Otros', 'Otros'),
    ]

comunas_santiago = [
    ('Santiago', 'Santiago'),
    ('Maipú', 'Maipú'),
    ('Providencia', 'Providencia'),
    ('Las Condes', 'Las Condes'),
    ('Ñuñoa', 'Ñuñoa'),
    ('La Florida', 'La Florida'),
    ('La Cisterna', 'La Cisterna'),
    ('Puente Alto', 'Puente Alto'),
    ('San Bernardo', 'San Bernardo')
]

estado = [
    ('Enviado', 'Enviado'),
    ('Recibido', 'Recibido'),
    ('En bodega', 'En bodega'),
]

class Producto(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos',null=True)
    precio = models.IntegerField(validators=[MinValueValidator(1)])
    stock= models.SmallIntegerField(validators=[MinValueValidator(1)])
    categoria = models.CharField(max_length=20, choices=categorias)

class Carrito(models.Model):
    cantidad = models.PositiveSmallIntegerField()
    subtotal = models.IntegerField(validators=[MinValueValidator(1)])
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)



class OrdenCompra(models.Model):
    f_compra = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField()
    direccion = models.CharField(max_length=30)
    recibe = models.CharField(max_length = 40)
    comuna = models.CharField(max_length= 20 , choices=comunas_santiago)
    estado = models.CharField(max_length=20 , choices=estado, default='En bodega')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
#Copia de la compra del producto
class compraProducto(models.Model):
    cantidad = models.PositiveSmallIntegerField()
    subtotal = models.IntegerField(validators=[MinValueValidator(1)])
    nombre = models.CharField(max_length=30,default='')
    compra = models.ForeignKey(OrdenCompra,on_delete=models.CASCADE)
