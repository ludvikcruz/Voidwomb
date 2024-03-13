def get_cart(request):
    """Obter o carrinho de compras da sessão."""
    cart = request.session.get('cart', {})
    return cart

def add_to_cart(request, produto_id):
    cart = request.session.get('cart', {})
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
        request.session['cart'] = cart

def clear_cart(request):
    """Limpar o carrinho."""
    request.session['cart'] = {}
