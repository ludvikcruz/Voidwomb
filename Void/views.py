from django.shortcuts import get_object_or_404, render,redirect

from payment.carrinho import add_to_cart
from .models import Evento, Produto, ProdutoTamanho, country
from django.core.mail import send_mail
from django.http import HttpResponse

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
    produtos = Produto.objects.all()
    
    
    return render(request,'store.html',{'produtos':produtos})

def about(request):
    return render(request,'about.html')

def adicionar_ao_carrinho(request, produto_id):
    cart = request.session.get('carrinho', {})

    product_id_str = str(produto_id)  # Certifique-se de que o ID seja uma string para evitar problemas de chave em dicionários.
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session['carrinho'] = cart
    return redirect('store')

def adicionar_dentro_carrinho(request, produto_id):
    cart = request.session.get('carrinho', {})
    if request.method == 'POST':
        product_id_str = str(produto_id)  # Convert product ID to string to use as a dictionary key.
        quantity = int(request.POST.get('quantity'))  # Get quantity from request, default to 1 if not provided.

        if product_id_str in cart:
            cart[product_id_str] += quantity
        else:
            cart[product_id_str] = quantity

        request.session['carrinho'] = cart  # Update the session with the new cart state.
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
    return redirect('carrinho')

def carrinho(request):
    countrys = country.objects.all()
    carrinho = request.session.get('carrinho', {})
    itens_carrinho = []
    total = 0
    for produto_id, quantidade in carrinho.items():
        produto = Produto.objects.get(id=produto_id)
        subtotal = produto.preco * quantidade
        total += subtotal
        itens_carrinho.append({
            'produto_id':produto.id,
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal,
        })

    return render(request, 'store/dados_encomenda.html', {'itens_carrinho': itens_carrinho, 'total': total,'countrys':countrys})

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


