# Generated by Django 5.0.4 on 2024-04-21 21:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0004_remove_compraproducto_producto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordencompra',
            name='compra',
        ),
        migrations.AddField(
            model_name='ordencompra',
            name='compra',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='productos.compraproducto'),
            preserve_default=False,
        ),
    ]
