from django.db import models
from django.core.validators import MinValueValidator

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
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock= models.SmallIntegerField(validators=[MinValueValidator(1)])
    categoria = models.CharField(max_length=20, choices=categorias)

