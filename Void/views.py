import json
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.contrib import messages
from payment.carrinho import add_to_cart
from .models import Evento, Produto, ProdutoTamanho, country
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect

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

def adicionar_ao_carrinho(request, produto_id):
    cart = request.session.get('carrinho', {})

    # Busca o produto pelo ID ou retorna uma resposta 404 se não encontrado
    produto = get_object_or_404(Produto, id=produto_id)

    product_id_str = str(produto_id)  # Certifique-se de que o ID seja uma string para evitar problemas de chave em dicionários.
    
    # Verifica se o produto já está no carrinho e se tem estoque suficiente
    quantidade_atual = cart.get(product_id_str, 0)
    if quantidade_atual < produto.stock:  # Verifica o estoque antes de adicionar ou incrementar
        if product_id_str in cart:
            cart[product_id_str] += 1
        else:
            messages.error(request, f'Pedido acima do stock atual. Atualmente, temos apenas {produto.stock} unidades de {produto.nome} em estoque.')
            cart[product_id_str] = 1
        request.session['carrinho'] = cart
        # Você pode adicionar alguma mensagem de sucesso aqui
    else:
        messages.error(request, f'Pedido acima do stock atual. Atualmente, temos apenas {produto.stock} unidades de {produto.nome} em estoque.')
        return redirect('store')

    return redirect('store')

def adicionar_dentro_carrinho(request, produto_id):
    cart = request.session.get('carrinho', {})

    # Busca o produto pelo ID ou retorna uma resposta 404 se não encontrado
    produto = get_object_or_404(Produto, id=produto_id)

    product_id_str = str(produto_id)  # Certifique-se de que o ID seja uma string para evitar problemas de chave em dicionários.
    
    # Verifica se o produto já está no carrinho e se tem estoque suficiente
    quantidade_atual = cart.get(product_id_str, 0)
    if quantidade_atual < produto.stock:  # Verifica o estoque antes de adicionar ou incrementar
        if product_id_str in cart:
            cart[product_id_str] += 1
            messages.success(request, f'Produto {produto.nome} adicionado ao carrinho com sucesso.')
        else:
            cart[product_id_str] = 1
        request.session['carrinho'] = cart
        # Você pode adicionar alguma mensagem de sucesso aqui
    else:
        messages.error(request, f'Pedido acima do stock atual. Atualmente, temos apenas {produto.stock} unidades de {produto.nome} em estoque.')
        return redirect('carrinho')

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



