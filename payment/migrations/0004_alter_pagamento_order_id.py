# Generated by Django 5.0.1 on 2024-03-28 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_pagamento_remove_sale_id_produto_itemdocarrinho_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamento',
            name='order_id',
            field=models.CharField(max_length=100),
        ),
    ]
