from django import forms
from django.forms import inlineformset_factory

from modulos.productos.models import Producto

# class ProductoForm(forms.ModelForm):
#     class Meta:
#         model = Producto
#         fields = ('nombre', 'descripcion','imagen', 'precio', 'stock', 'categoria')

# class ImagenForm(forms.ModelForm):
#     class Meta:
#         model = Imagen
#         fields = ('imagen', )

# ImagenFormSet  = inlineformset_factory(Producto, Imagen, form=ImagenForm, extra=1,can_delete=True)



class productoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('nombre','descripcion','precio','imagen','stock','categoria')
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa un nombre'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control mt-2','placeholder':'Ingresa una descripcion'}),
            'precio': forms.NumberInput(attrs = {'class':'form-control mt-2','placeholder':'Ingresa el precio'}),
            'imagen':forms.FileInput(attrs = {'class':'form-control mt-2'}),
            'stock': forms.NumberInput(attrs = {'class':'form-control mt-2','placeholder':'Ingresa el stock'}),
            'categoria': forms.Select(attrs = {'class':'form-control mt-2','placeholder':'Selecciona una categoria'}),
        }

