"""Voidwomb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from Void import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='home'),
    path('rituals',views.rituals,name = 'rituals'),
    path('about',views.about,name = 'about'),
    path('contact',views.contact,name = 'contact'),
    path('store',views.store,name = 'store'),
    path('payment/', include('payment.urls')),
    path('Adm/',include('Adm.urls')),
    path('cart/add/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('cart/ad/<int:produto_id>/', views.adicionar_dentro_carrinho, name='adicionar_dentro_carrinho'), 
    path('cart/delete/<int:produto_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('cart/',views.carrinho,name='carrinho'),
    path('store/product/<int:produto_id>',views.produto,name='produto'),
    path('cart/details',views.pessoa_encomenda,name='pessoa_encomenda'),
    path('cart/payment/',views.payout,name='pay'),
    path('api/request/fetchstock',views.verificar_estoque,name='verify')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)