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

def adicionar_ao_carrinho(request, produto_id):
    cart = request.session.get('carrinho', {})

    product_id_str = str(produto_id)
    if product_id_str in cart:
        # Verifica se o valor correspondente a product_id_str é um dicionário
        if isinstance(cart[product_id_str], dict):
            cart[product_id_str]['quantidade'] += 1
        else:
            # Se for um inteiro, substitui por um dicionário
            cart[product_id_str] = {'quantidade': cart[product_id_str] + 1, 'tamanho': 'único'}
    else:
        cart[product_id_str] = {'quantidade': 1, 'tamanho': 'único'}

    request.session['carrinho'] = cart
    return redirect('store')



def adicionar_dentro_carrinho(request, produto_id):
    cart = request.session.get('carrinho', {})

    product_id_str = str(produto_id)
    if product_id_str in cart:
        # Verifica se o valor correspondente a product_id_str é um dicionário
        if isinstance(cart[product_id_str], dict):
            cart[product_id_str]['quantidade'] += 1
        else:
            # Se for um inteiro, substitui por um dicionário
            cart[product_id_str] = {'quantidade': cart[product_id_str] + 1, 'tamanho': 'único'}
    else:
        cart[product_id_str] = {'quantidade': 1, 'tamanho': 'único'}

    request.session['carrinho'] = cart
    return redirect('carrinho')



def adicionar_roupa(request, produto_id):
    cart = request.session.get('carrinho', {})
    produto = get_object_or_404(Produto, id=produto_id)
    quantidade_a_adicionar = int(request.POST.get('quantidade', 1))

    # Verifica se foi enviado um tamanho no formulário
    tamanho_id = request.POST.get('size')
    if not tamanho_id:
        messages.error(request, 'É necessário selecionar um tamanho.')
        return redirect('carrinho')

    # Verifica se o tamanho é válido para o produto
    tamanho_objeto = get_object_or_404(ProdutoTamanho, id=tamanho_id, produto=produto)

    # Define a chave do carrinho baseada no ID do produto e do tamanho
    chave_carrinho = f"{produto_id}"

    # Atualiza ou adiciona o item ao carrinho
    if chave_carrinho in cart:
        cart[chave_carrinho]['quantidade'] += quantidade_a_adicionar
    else:
        cart[chave_carrinho] = {'quantidade': quantidade_a_adicionar, 'tamanho': tamanho_id}

    # Verifica estoque
    if cart[chave_carrinho]['quantidade'] > tamanho_objeto.stock_por_tamanho:
        messages.error(request, f'It is not possible to add the desired quantity to the cart. Available stock for the size {tamanho_objeto.tamanho}: {tamanho_objeto.stock_por_tamanho}.')
        return redirect('carrinho')

    request.session['carrinho'] = cart
    messages.success(request, f'{quantidade_a_adicionar} pieces of {produto.nome} ({tamanho_objeto.tamanho}) added to the cart.')
    return redirect('store')

   
def adicionar_roupa_dentro_carrinho(request, produto_id):
    cart = request.session.get('carrinho', {})
    produto = get_object_or_404(Produto, id=produto_id)
    
    # Define a chave do carrinho baseada no ID do produto
    chave_carrinho = f"{produto_id}"

    # Verifica se o produto está presente no carrinho
    if chave_carrinho in cart:
        # Incrementa a quantidade do produto
        cart[chave_carrinho]['quantidade'] += 1
    else:
        cart[chave_carrinho] = {'quantidade': quantidade_a_adicionar, 'tamanho': tamanho if tamanho else 'único'}

    # Verifica estoque se necessário
    if tamanho:
        tamanho_objeto = get_object_or_404(ProdutoTamanho, produto=produto, tamanho=tamanho)
        if cart[chave_carrinho]['quantidade'] >= tamanho_objeto.stock_por_tamanho:
            messages.error(request, f'It is not possible to add the desired quantity to the cart. Available stock for the size {tamanho}: {tamanho_objeto.estoque}.')
            return HttpResponseRedirect(reverse('carrinho'))

    request.session['carrinho'] = cart
    messages.success(request, f'{quantidade_a_adicionar} pieces of {produto.nome} added to the cart.')
    return HttpResponseRedirect(reverse('carrinho'))


def remover_do_carrinho(request, produto_id):
    cart = request.session.get('carrinho', {})

    product_id_str = str(produto_id)
    if product_id_str in cart:
        if cart[product_id_str]['quantidade'] > 1:
            cart[product_id_str]['quantidade'] -= 1  # Decrementa a quantidade do item
        else:
            del cart[product_id_str]  # Remove o item do carrinho se a quantidade for 1 ou menos

    request.session['carrinho'] = cart
    return HttpResponseRedirect(reverse('carrinho'))

def remover_roupa_do_carrinho(request, produto_id, tamanho_id=None):
    cart = request.session.get('carrinho', {})

    chave = f"{produto_id}_{tamanho_id}" if tamanho_id else str(produto_id)

    if chave in cart:
        del cart[chave]
        request.session['carrinho'] = cart
        messages.success(request, 'Produto removido do carrinho com sucesso.')
    else:
        messages.error(request, 'O produto selecionado não está no carrinho.')

    return HttpResponseRedirect(reverse('carrinho'))





# def carrinho(request):
#     countrys = country.objects.all()
#     cart = request.session.get('carrinho', {})
#     itens_carrinho = []
#     total = 0
#     print(cart)
#     for chave, info_produto in cart.items():
#         produto_id, tamanho_id = chave.split('_') if '_' in chave else (chave, None)
#         produto = get_object_or_404(Produto, id=produto_id)
#         tamanho = get_object_or_404(ProdutoTamanho, id=tamanho_id) if tamanho_id else None
#         quantidade = info_produto['quantidade']  
#         if quantidade > produto.stock:
#             messages.error(request, f'Stock insuficiente para {produto.nome}. Disponíveis: {produto.stock}.')
#             # Adiciona ao carrinho mas marca como inativo e não adiciona ao total
#             itens_carrinho.append({
#                 'produto_id': produto.id,
#                 'produto': produto,
#                 'quantidade': quantidade,
#                 'subtotal': produto.preco * min(quantidade, produto.stock),
#                 'tamanho': tamanho,
#                 'tamanho_nome': tamanho.tamanho if tamanho else 'único',
#                 'ativo': False,  
#             })
#         else:
#             subtotal = produto.preco * quantidade
#             total += subtotal  
#             itens_carrinho.append({
#                 'produto_id': produto.id,
#                 'produto': produto,
#                 'quantidade': quantidade,
#                 'subtotal': subtotal,
#                 'tamanho': tamanho,
#                 'tamanho_nome': tamanho.tamanho if tamanho else 'único',
#                 'ativo': True,
#             })

#     return render(request, 'store/dados_encomenda.html', {
#         'itens_carrinho': itens_carrinho,
#         'total': total,
#         'countrys': countrys,
#     })
def carrinho(request):
    countrys = country.objects.all()
    cart = request.session.get('carrinho', {})
    itens_carrinho = []
    total = 0
    print(cart)
    for produto_id, info_produto in cart.items():
        produto = get_object_or_404(Produto, id=produto_id)
        tamanho_id = info_produto.get('tamanho')
        tamanho = None
        tamanho_nome = 'único'  # Definindo como 'único' por padrão

        if tamanho_id != 'único':
            tamanho = get_object_or_404(ProdutoTamanho, id=tamanho_id)
            tamanho_nome = tamanho.tamanho

        quantidade = info_produto['quantidade']  

        if quantidade > produto.stock:
            messages.error(request, f'Not enough stock of {produto.nome}. Available: {produto.stock}.')
            # Adiciona ao carrinho mas marca como inativo e não adiciona ao total
            itens_carrinho.append({
                'produto_id': produto.id,
                'produto': produto,
                'quantidade': quantidade,
                'subtotal': produto.preco * min(quantidade, produto.stock),
                'tamanho': tamanho,
                'tamanho_nome': tamanho_nome,
                'ativo': False,  
            })
        else:
            subtotal = produto.preco * quantidade
            total += subtotal  
            itens_carrinho.append({
                'produto_id': produto.id,
                'produto': produto,
                'quantidade': quantidade,
                'subtotal': subtotal,
                'tamanho': tamanho,
                'tamanho_nome': tamanho_nome,
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



