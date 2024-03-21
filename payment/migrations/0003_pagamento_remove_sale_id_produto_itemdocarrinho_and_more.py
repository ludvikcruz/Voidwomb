# Generated by Django 5.0.1 on 2024-03-21 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_itemcarrinho'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('endereco', models.CharField(max_length=255)),
                ('codigo_postal', models.CharField(max_length=20)),
                ('cidade', models.CharField(max_length=100)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_pagamento', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='sale',
            name='id_produto',
        ),
        migrations.CreateModel(
            name='ItemDoCarrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produto_id', models.CharField(max_length=100)),
                ('nome', models.CharField(max_length=255)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantidade', models.IntegerField()),
                ('pagamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='payment.pagamento')),
            ],
        ),
        migrations.DeleteModel(
            name='ItemCarrinho',
        ),
        migrations.DeleteModel(
            name='Sale',
        ),
    ]
