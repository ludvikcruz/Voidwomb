from Void.models import Produto


def get_cart(request):
    """Obter o carrinho de compras da sessão."""
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
    return carrinho

def add_to_cart(request, produto_id):
    cart = request.session.get('carrinho', {})
    # Adiciona o produto ao carrinho ou atualiza a quantidade
    if produto_id in cart:
        cart[produto_id] += 1
    else:
        cart[produto_id] = 1

    request.session['cart'] = cart

def remove_from_cart(request, produto_id):
    """Remover um produto do carrinho."""
    cart = get_cart(request)
    if produto_id in cart:
        del cart[produto_id]
        request.session['carrinho'] = cart

def clear_cart(request):
    """Limpar o carrinho."""
    request.session['carrinho'] = {}
