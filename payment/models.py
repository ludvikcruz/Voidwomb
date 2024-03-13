from django.db import models
from Void.models import Produto

class Sale(models.Model):
    product_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    buyer_email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)
    id_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product_name} ({self.quantity}) - {self.date}"
    
    
    
class ItemCarrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade} de {self.produto.nome}"