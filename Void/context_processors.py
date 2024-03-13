def cart_context(request):
    cart = request.session.get('carrinho', {})
    cart_items_count = sum(item for item in cart.values())
    return {'cart_items_count': cart_items_count}