# Generated by Django 5.0.1 on 2024-03-15 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Void', '0016_alter_produto_descricao_alter_produto_stock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produtotamanho',
            old_name='produto',
            new_name='produto_id',
        ),
    ]
