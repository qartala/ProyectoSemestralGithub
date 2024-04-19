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

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
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
