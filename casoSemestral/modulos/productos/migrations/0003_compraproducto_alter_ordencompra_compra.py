# Generated by Django 5.0.4 on 2024-04-21 02:16

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_ordencompra_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='compraProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveSmallIntegerField()),
                ('subtotal', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
            ],
        ),
        migrations.AlterField(
            model_name='ordencompra',
            name='compra',
            field=models.ManyToManyField(to='productos.compraproducto'),
        ),
    ]
