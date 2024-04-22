def cart_context(request):
    cart = request.session.get('carrinho', {})
    cart_items_count = sum(item.get('quantidade', 0) if isinstance(item, dict) else 0 for item in cart.values())
    request.session.set_expiry(300)
    return {'cart_items_count': cart_items_count}
