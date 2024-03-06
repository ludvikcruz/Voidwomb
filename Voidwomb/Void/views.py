from django.shortcuts import render
from .models import Produto

def index(request):
    return render(request,'index.html')


def contact(request):
    return render(request,'contact.html')

def rituals(request):
    return render(request,'rituals.html')

def store(request):
    produtos = Produto.objects.all()
    
    return render(request,'store.html',{'produtos':produtos})

def about(request):
    return render(request,'about.html')