from django.db import models

# Create your models here.
class Produto(models.Model):
    CATEGORIAS = [
        ('cd', 'CD'),
        ('roupa', 'Roupa'),
        ('vinil', 'Vinil'),
    ]
    TAMANHOS = [
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('XXl', 'XXL'),
    ]

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    sku = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, blank=True, null=True)
    cor = models.CharField(max_length=50, blank=True, null=True)
    tamanho = models.CharField(max_length=50,choices=TAMANHOS, blank=True, null=True)
    imagem = models.ImageField(upload_to='produtos_imagens/', blank=True, null=True ,default='produtos_imagens/Tshirt-AOCD.jpg')
    vendas = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nome
    
    
class Tamanho(models.Model):
    pass

class country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField()
    acronimo=models.CharField()
    

class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    data = models.CharField()
    localizacao = models.CharField(max_length=200)
    hiperligacao = models.URLField()
    foto = models.ImageField(upload_to='eventos_fotos/')

    def __str__(self):
        return self.titulo