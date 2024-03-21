import json
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.contrib import messages
from payment.carrinho import add_to_cart
from .models import Evento, Produto, ProdutoTamanho, country
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST

def index(request):
    return render(request,'index.html')


def contact(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('body')

        # Construa a mensagem de e-mail
        full_message = f"Recebido de: {email}\n\n{message}"

        # Enviar e-mail
        send_mail(
            subject=subject,
            message=full_message,
            from_email=email,
            recipient_list=['voidwomb.band@gmail.com'],  # Substitua pelo e-mail que receberá a mensagem
        )
        
        return redirect('contact')
    return render(request,'contact.html')

def rituals(request):
    eventos = Evento.objects.all()
    return render(request,'rituals.html',{'eventos':eventos})

def store(request):
    produtos = Produto.objects.filter(stock__gt=0)
    
    
    return render(request,'store.html',{'produtos':produtos})

def about(request):
    return render(request,'about.html')

@require_POST  # Assegura que esta view só possa ser acessada via método POST
def adicionar_ao_carrinho(request, produto_id):
    cart = request.session.get('carrinho', {})

    produto = get_object_or_404(Produto, id=produto_id)
    tamanho = request.POST.get('tamanho')
    quantidade_a_adicionar = int(request.POST.get('quantidade', 1))  # Assume 1 se não especificado

    # Chave única para identificar produto e tamanho no carrinho
    chave_carrinho = f"{produto_id}_{tamanho}"

    # Verifica se o produto já está no carrinho
    if chave_carrinho in cart:
        item_atual = cart[chave_carrinho]
        quantidade_total = item_atual['quantidade'] + quantidade_a_adicionar
    else:
        quantidade_total = quantidade_a_adicionar

    # Busca o objeto Tamanho para verificar o estoque específico
    tamanho_objeto = get_object_or_404(ProdutoTamanho, produto=produto, nome=tamanho)

    if quantidade_total <= tamanho_objeto.estoque:
        # Atualiza ou adiciona o item com a nova quantidade
        cart[chave_carrinho] = {'quantidade': quantidade_total, 'tamanho': tamanho}
        request.session['carrinho'] = cart
        messages.success(request, f'{quantidade_a_adicionar} unidades do tamanho {tamanho} de {produto.nome} adicionadas ao carrinho.')
        return redirect('store')
    else:
        # Quantidade solicitada excede o estoque disponível
        messages.error(request, f'Não é possível adicionar a quantidade desejada ao carrinho. Quantidade em estoque disponível para o tamanho {tamanho}: {tamanho_objeto.estoque}.')

    return redirect('store')

@require_POST  # Assegura que esta view só possa ser acessada via método POST
def adicionar_dentro_carrinho(request, produto_id):
    cart = request.session.get('carrinho', {})

    produto = get_object_or_404(Produto, id=produto_id)
    tamanho = request.POST.get('tamanho')
    quantidade_a_adicionar = int(request.POST.get('quantidade', 1))  # Assume 1 se não especificado

    # Chave única para identificar produto e tamanho no carrinho
    chave_carrinho = f"{produto_id}_{tamanho}"

    # Verifica se o produto já está no carrinho
    if chave_carrinho in cart:
        item_atual = cart[chave_carrinho]
        quantidade_total = item_atual['quantidade'] + quantidade_a_adicionar
    else:
        quantidade_total = quantidade_a_adicionar

    # Busca o objeto Tamanho para verificar o estoque específico
    tamanho_objeto = get_object_or_404(ProdutoTamanho, produto=produto, nome=tamanho)

    if quantidade_total <= tamanho_objeto.estoque:
        # Atualiza ou adiciona o item com a nova quantidade
        cart[chave_carrinho] = {'quantidade': quantidade_total, 'tamanho': tamanho}
        request.session['carrinho'] = cart
        messages.success(request, f'{quantidade_a_adicionar} unidades do tamanho {tamanho} de {produto.nome} adicionadas ao carrinho.')
    else:
        # Quantidade solicitada excede o estoque disponível
        messages.error(request, f'Não é possível adicionar a quantidade desejada ao carrinho. Quantidade em estoque disponível para o tamanho {tamanho}: {tamanho_objeto.estoque}.')

    return redirect('carrinho')

def remover_do_carrinho(request, produto_id):
    cart = request.session.get('carrinho', {})

    product_id_str = str(produto_id)  # Certifique-se de que o ID seja uma string para evitar problemas de chave em dicionários.
    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1  # Decrementa a quantidade do item
        else:
            del cart[product_id_str]  # Remove o item do carrinho se a quantidade for 1 ou menos

    request.session['carrinho'] = cart
    return HttpResponseRedirect(reverse('carrinho'))

def carrinho(request):
    countrys = country.objects.all()
    cart = request.session.get('carrinho', {})
    itens_carrinho = []
    total = 0

    for produto_id, quantidade in cart.items():
        produto = get_object_or_404(Produto, id=produto_id)
        if quantidade > produto.stock:
            messages.error(request, f'Estoque insuficiente para {produto.nome}. Disponíveis: {produto.stock}.')
            # Adiciona ao carrinho mas marca como inativo e não adiciona ao total
            itens_carrinho.append({
                'produto_id': produto.id,
                'produto': produto,
                'quantidade': quantidade,
                'subtotal': produto.preco * min(quantidade, produto.stock),
                'ativo': False,  # Produto inativo devido a estoque insuficiente
            })
        else:
            subtotal = produto.preco * quantidade
            total += subtotal  # Adiciona ao total apenas se ativo
            itens_carrinho.append({
                'produto_id': produto.id,
                'produto': produto,
                'quantidade': quantidade,
                'subtotal': subtotal,
                'ativo': True,
            })

    return render(request, 'store/dados_encomenda.html', {
        'itens_carrinho': itens_carrinho,
        'total': total,
        'countrys': countrys,
    })
def produto(request, produto_id):
    # Utiliza get_object_or_404 para tentar obter o produto correspondente ao ID.
    # Caso não exista, retorna uma página 404 automaticamente.
    produto = get_object_or_404(Produto, id=produto_id)
    tamanhos_disponiveis = ProdutoTamanho.objects.filter(produto_id=produto,stock_por_tamanho__gt=0)
    
    context={
        'produto': produto,
        'tamanhos_disponiveis': tamanhos_disponiveis
    }
    # Passa o produto obtido para o template.
    return render(request, 'produto.html', context)

def pessoa_encomenda(request):
    return render(request,'store/pessoa_encomenda.html')

def payout(request):
    return render(request,'store/payment.html')


def remover_dentro_carrinho(request, produto_id):
    # Acessa o carrinho armazenado na sessão
    carrinho = request.session.get('carrinho', {})

    # Converte o produto_id para string, pois as chaves do dicionário estão em string
    product_id_str = str(produto_id)

    # Verifica se o produto existe no carrinho e o remove
    if product_id_str in carrinho:
        del carrinho[product_id_str]
        request.session['carrinho'] = carrinho  # Salva o carrinho atualizado na sessão

    # Redireciona para a página do carrinho ou para outra página de sua escolha
    return redirect('carrinho')



