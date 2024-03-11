from django.db import models

# Create your models here.
class Produto(models.Model):
    CATEGORIAS = [
        ('cd', 'CD'),
        ('roupa', 'Roupa'),
        ('vinil', 'Vinil'),
    ]

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    sku = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, blank=True, null=True)
    cor = models.CharField(max_length=50, blank=True, null=True)
    tamanho = models.CharField(max_length=50, blank=True, null=True)
    imagem = models.ImageField(upload_to='produtos_imagens/', blank=True, null=True)


    def __str__(self):
        return self.nome
    
class rituals(models.Model):
    id = models.AutoField(primary_key=True)