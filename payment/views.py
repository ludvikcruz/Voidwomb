import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Void.models import Produto, ProdutoTamanho
from .models import Pagamento, ItemDoCarrinho

@csrf_exempt
@require_http_methods(["POST"])
def registrar_pagamento(request):
    # Captura o token único do cabeçalho da solicitação
    token_unico = request.headers.get('Token-Unico')

    # Valida o formato do token único
    if not token_unico or not re.match(r'^tkn_[a-zA-Z0-9]+$', token_unico):
        return JsonResponse({"erro": "Token inválido ou ausente."}, status=400)

    try:
        data = json.loads(request.body)

        # Prossegue para criar o registro de pagamento apenas se o token é válido
        pagamento = Pagamento.objects.create(
            order_id=data['orderID'],
            email=data['customerInfo']['email'],
            endereco=data['customerInfo']['address'],
            codigo_postal=data['customerInfo']['postalCode'],
            cidade=data['customerInfo']['city'],
            total=data['carrinho']['total']
        )
        for item in data['carrinho']['itens']:
                produto = Produto.objects.get(id=item['produto_id'])
                quantidade_vendida = item['quantidade']
                tamanho_nome = item.get('tamanho')  # Pode ser None se não aplicável

                if tamanho_nome:
                    tamanho = ProdutoTamanho.objects.get(produto=produto, nome=tamanho_nome)
                    if tamanho.estoque >= quantidade_vendida:
                        tamanho.estoque -= quantidade_vendida
                        tamanho.save()
                        produto.estoque_total -= quantidade_vendida  # Atualiza estoque total
                        produto.save()
                    else:
                        raise ValueError("Estoque insuficiente para o tamanho selecionado.")
                else:
                    if produto.estoque_total >= quantidade_vendida:
                        produto.estoque_total -= quantidade_vendida
                        produto.save()
                    else:
                        raise ValueError("Estoque insuficiente para o produto selecionado.")

        return JsonResponse({"mensagem": "Pagamento registrado, estoque atualizado."}, status=201)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=400)
