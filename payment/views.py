from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse
import paypalrestsdk
from django.core.mail import send_mail
from Void.models import Produto

# Configuração do PayPal
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

def get_paypal_items_from_cart(request):
    carrinho = request.session.get('carrinho', {})
    itens_paypal = []
    total = 0
    for produto_id, quantidade in carrinho.items():
        produto = Produto.objects.get(id=produto_id)
        subtotal = produto.preco * quantidade
        total += subtotal
        itens_paypal.append({
            "name": produto.nome,
            "sku": produto_id,
            "price": str(produto.preco),
            "currency": "EUR",
            "quantity": quantidade,
        })
    return itens_paypal, total

def create_payment(request):
    itens_paypal, total = get_paypal_items_from_cart(request)
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": "http://localhost:8000/payment/execute/",
            "cancel_url": "http://localhost:8000/payment/cancel/",
        },
        "transactions": [{
            "item_list": {
                "items": itens_paypal,
            },
            "amount": {
                "total": f"{total:.2f}",
                "currency": "USD",
            },
            "description": "Descrição da compra no carrinho.",
        }]
    })

    if payment.create():
        print("Payment created successfully")
        for link in payment.links:
            if link.rel == "approval_url":
                # Captura a URL de aprovação para redirecionar o usuário ao PayPal
                approval_url = str(link.href)
                return redirect(approval_url)
    else:
        print(payment.error)
    return JsonResponse({"error": "Falha na criação do pagamento"})

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        print("Payment execute successfully")
        
        # Enviar e-mail de confirmação
        send_payment_confirmation_email(payment)

        # Aqui você pode redirecionar para uma página de sucesso ou retornar uma resposta de sucesso
        return HttpResponse("Pagamento concluído com sucesso.")
    else:
        print(payment.error)  # Logging the error
        # Aqui você pode redirecionar para uma página de erro ou retornar uma resposta de erro
        return HttpResponse("Falha na execução do pagamento.")

def send_payment_confirmation_email(payment):
    subject = 'Confirmação de Pagamento'
    message = f'O pagamento de {payment.transactions[0].amount.total} {payment.transactions[0].amount.currency} foi concluído com sucesso.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['emaildodestinatario@example.com']
    send_mail(subject, message, email_from, recipient_list)


def payment_cancelled(request):
    # Aqui você pode adicionar qualquer lógica que precisa ser executada quando o pagamento é cancelado
    # Por exemplo, mostrar uma mensagem ao usuário, registrar o evento, etc.
    return HttpResponse("Pagamento cancelado. Se você encontrou um problema com o pagamento, por favor, tente novamente ou entre em contato conosco.")
