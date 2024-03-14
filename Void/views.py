from django.shortcuts import render,redirect

from payment.carrinho import add_to_cart
from .models import Produto
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
    return render(request,'rituals.html')

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

def carrinho(request):
    carrinho = request.session.get('carrinho', {})
    itens_carrinho = []
    total = 0
    for produto_id, quantidade in carrinho.items():
        produto = Produto.objects.get(id=produto_id)
        subtotal = produto.preco * quantidade
        total += subtotal
        itens_carrinho.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal,
        })

    return render(request, 'store/dados_encomenda.html', {'itens_carrinho': itens_carrinho, 'total': total})