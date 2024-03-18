from django.db import models
from PIL import Image
from django.core.files.storage import default_storage
# Create your models here.
class Produto(models.Model):
    CATEGORIAS = [
        ('cd', 'CD'),
        ('roupa', 'Roupa'),
        ('vinil', 'Vinil'),
    ]
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(blank=True)
    sku = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, blank=True, null=True)
    cor = models.CharField(max_length=50, blank=True, null=True)
    imagem = models.ImageField(upload_to='produtos_imagens/', blank=True, null=True, default='produtos_imagens/Tshirt-AOCD.jpg')
    vendas = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nome
    def save(self, *args, **kwargs):
        if self.pk:  # verifica se o objeto já existe
            old_obj = Produto.objects.get(pk=self.pk)
            if old_obj.imagem and old_obj.imagem != self.imagem and default_storage.exists(old_obj.imagem.name):
                default_storage.delete(old_obj.imagem.name)
                
        super().save(*args, **kwargs)  # Chama o método save original para salvar o objeto

        if self.imagem:  # Verifica se uma imagem foi enviada
            img = Image.open(self.imagem.path)  # Abre a imagem usando Pillow

            # Define o tamanho máximo desejado (por exemplo, 800x800)
            max_size = (800, 800)

            # Redimensiona a imagem, preservando a proporção
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Salva a imagem redimensionada, substituindo a original
            img.save(self.imagem.path)
    def delete(self, *args, **kwargs):
        if self.imagem and default_storage.exists(self.imagem.name):
            default_storage.delete(self.imagem.name)
        super().delete(*args, **kwargs)
        
         
class ProdutoTamanho(models.Model):
    TAMANHOS = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    ]
    # Aqui a ForeignKey deve apontar para Produto, como já está, mas sem o sublinhado no nome do campo
    produto_id = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='tamanhos')
    tamanho = models.CharField(max_length=50, choices=TAMANHOS)
    stock_por_tamanho = models.IntegerField()

    def __str__(self):
        return f"{self.produto.nome} - {self.tamanho}"

class country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField()
    acronimo=models.CharField()
    shipping = models.FloatField(default = 6.5)
    

class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    data = models.CharField()
    localizacao = models.CharField(max_length=200)
    hiperligacao = models.URLField()
    foto = models.ImageField(upload_to='eventos_fotos/')

    def __str__(self):
        return self.titulo
    def save(self, *args, **kwargs):
        if self.pk:  # verifica se o objeto já existe
            old_obj = Evento.objects.get(pk=self.pk)
            if old_obj.foto and old_obj.foto != self.foto and default_storage.exists(old_obj.foto.name):
                default_storage.delete(old_obj.foto.name)
        super().save(*args, **kwargs)  # Chama o método save original para salvar o objeto

        if self.foto:  # Verifica se uma imagem foi enviada
            img = Image.open(self.foto.path)  # Abre a imagem usando Pillow

            # Define o tamanho máximo desejado (por exemplo, 800x800)
            max_size = (800, 800)

            # Redimensiona a imagem, preservando a proporção
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Salva a imagem redimensionada, substituindo a original
            img.save(self.foto.path)
            
    def delete(self, *args, **kwargs):
        if self.foto and default_storage.exists(self.foto.name):
            default_storage.delete(self.foto.name)
        super().delete(*args, **kwargs)     