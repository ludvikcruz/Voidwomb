# def cart_context(request):
#     cart = request.session.get('carrinho', {})
#     cart_items_count = sum(item.get('quantidade', 0) if isinstance(item, dict) else 0 for item in cart.values())
#     request.session.set_expiry(300)
#     return {'cart_items_count': cart_items_count}
from django.shortcuts import get_object_or_404

from Void.models import Produto


def cart_context(request):
    cart = request.session.get('carrinho', {})
    cart_items_count = sum(item.get('quantidade', 0) if isinstance(item, dict) else 0 for item in cart.values())
    
    # Verifica se o tempo do cookie expirou
    if 'carrinho' in request.session and request.session.get_expiry_age() <= 0:
        for product_id_str, item in cart.items():
            # Adiciona cada item de volta ao estoque
            produto = get_object_or_404(Produto, id=int(product_id_str))
            produto.estoque += item.get('quantidade', 0)
            produto.save()
        
        # Limpa o carrinho
        del request.session['carrinho']
    
    # Define o tempo de expiração da sessão para 300 segundos (5 minutos)
    request.session.set_expiry(300)
    
    return {'cart_items_count': cart_items_count}
