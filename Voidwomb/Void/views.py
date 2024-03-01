from django.shortcuts import render

def index(request):
    return render(request,'index.html')


def contact(request):
    return render(request,'contact.html')

def rituals(request):
    return render(request,'rituals.html')

def store(request):
    return render(request,'store.html')

def about(request):
    return render(request,'about.html')