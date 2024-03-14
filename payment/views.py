from django.shortcuts import redirect
import paypalrestsdk
from django.conf import settings
from django.http import JsonResponse

paypalrestsdk.configure({
  "mode": settings.PAYPAL_MODE,  # sandbox or live
  "client_id": settings.PAYPAL_CLIENT_ID,
  "client_secret": settings.PAYPAL_CLIENT_SECRET })

def create_payment(request):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:8000/payment/execute/",
            "cancel_url": "http://localhost:8000/payment/cancel/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "item",
                    "sku": "item",
                    "price": "5.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "5.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print("Payment created successfully")
        for link in payment.links:
            if link.rel == "approval_url":
                # Capture the approval_url to redirect the user to PayPal for payment approval
                approval_url = str(link.href)
                print("Redirect for approval: %s" % (approval_url))
                return redirect(approval_url)
    else:
        print(payment.error)
    return JsonResponse({"error": "Payment creation failed"})


def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        print("Payment execute successfully")
        # Aqui você pode adicionar lógica após o sucesso do pagamento, como enviar um e-mail
    else:
        print(payment.error)  # Logging the error
    # Redirecionar para uma página de confirmação/erro conforme necessário
