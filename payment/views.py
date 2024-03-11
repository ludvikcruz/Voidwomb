# payment/views.py
from django.shortcuts import redirect
from django.http import JsonResponse
import paypalrestsdk
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

def create_payment(request):
    paypalrestsdk.configure({
        "mode": "sandbox",  # Ou "live" para produção
        "client_id": env('PAYPAL_CLIENT_ID'),
        "client_secret": env('PAYPAL_CLIENT_SECRET')
    })

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": "URL_PARA_ONDE_O_USUARIO_DEVE_SER_REDIRECIONADO_APOS_PAGAMENTO",
            "cancel_url": "URL_PARA_ONDE_O_USUARIO_DEVE_SER_REDIRECIONADO_SE_CANCELAR_O_PAGAMENTO",
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Nome do item",
                    "sku": "Código SKU",
                    "price": "Preço unitário",
                    "currency": "Moeda",
                    "quantity": "Quantidade",
                }]
            },
            "amount": {
                "total": "Preço total",
                "currency": "EUR",
            },
            "description": "Descrição da transação",
        }]
    })

    if payment.create():
        # O pagamento foi criado com sucesso
        for link in payment.links:
            if link.rel == "approval_url":
                # Redireciona o usuário para o PayPal para aprovação
                return redirect(link.href)
    else:
        # Falha na criação do pagamento
        print(payment.error)

    return JsonResponse({'error': 'Erro ao criar o pagamento'})

