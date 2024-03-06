from django.db import models

# Create your models here.
class Produto(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    sku = models.CharField(max_length=100)

    def __str__(self):
        return self.nome