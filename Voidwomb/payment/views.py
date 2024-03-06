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
        # Configuração do pagamento aqui
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

