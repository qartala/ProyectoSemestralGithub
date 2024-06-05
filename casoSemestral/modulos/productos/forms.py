from django import forms
from django.forms import inlineformset_factory

from modulos.productos.models import Producto


class productoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('nombre','descripcion','precio','imagen','stock','categoria')
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa un nombre'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control mt-2','style': 'max-height: 100px; overflow-y: 100px;', 'rows': 3, 'cols': 15, 'placeholder': 'Descripción del producto'}),
            'precio': forms.NumberInput(attrs = {'class':'form-control mt-2','placeholder':'Ingresa el precio'}),
            'imagen':forms.FileInput(attrs = {'class':'form-control mt-2'}),
            'stock': forms.NumberInput(attrs = {'class':'form-control mt-2','placeholder':'Ingresa el stock'}),
            'categoria': forms.Select(attrs = {'class':'form-control mt-2','placeholder':'Selecciona una categoria'}),
        }

