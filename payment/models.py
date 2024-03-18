from django.db import models

class Pagamento(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    endereco = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=20)
    cidade = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pagamento {self.order_id}"

class ItemDoCarrinho(models.Model):
    pagamento = models.ForeignKey(Pagamento, related_name='itens', on_delete=models.CASCADE)
    produto_id = models.CharField(max_length=100)
    nome = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()

    def __str__(self):
        return f"Item {self.nome} do Pagamento {self.pagamento.order_id}"
