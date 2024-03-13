from django.shortcuts import render,redirect
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