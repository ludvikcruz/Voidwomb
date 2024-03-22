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
    #path('Adm/',include('Adm.urls')),
    
    
    path('Adm/',views.adm,name='admin'),
    
    
    
    #Paths dos produtos
    path('Adm/produtos/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('Adm/produtos/editar/<int:id>/', views.editar_produto, name='editar_produto'),
    path('Adm/produtos/eliminar/<int:id>/', views.eliminar_produto, name='eliminar_produto'),
    path('Adm/produtos/', views.lista_produtos_tamanhos, name='lista_produtos'),
    path('Adm/produtos/importExcel/', views.lista_produtos_tamanhos, name='upload_excel'),
    path('Adm/produtos/ExportExel/', views.exportar_produtos_csv, name='exportar_produtos'),
    path('Adm/caminho/para/eliminar/produtos/selecionados/', views.eliminar_selecionados, name='eliminar_produtos_selecionados'),
    path("Adm/produtos/tamanhos/adicionar", views.adicionar_tamanho, name="adicionar_tamanho"),
    path('Adm/produtos/tamanho/editar/<int:id>/', views.editar_tamanho, name='editar_tamanho'),
    path('Adm/produtos/tamanho/excluir/<int:id>/', views.excluir_tamanho, name='excluir_tamanho'),
    
    
    #Paths dos users
    path('Adm/users/login',views.login_view,name ='login'),
    path('Adm/users/logout',views.logout_view,name ='logout'),
 
    #path paises
    path('Adm/paises/', views.listar_paises, name='listar_paises'),
    path('Adm/paises/adicionar',views.paises_adicionar,name ='adicionar_paises'),
    path('Adm/paises/editar/<int:id>/', views.editar_pais, name='editar_pais'),
    path('Adm/paises/excluir/<int:id>/', views.excluir_pais, name='excluir_pais'),
    path('Adm/paises/import-countries/', views.listar_paises, name='import_countries'),

    #paths dos eventos
    path('Adm/eventos/', views.lista_eventos, name='lista_eventos'),
    path('Adm/eventos/add/', views.evento_add, name='evento_add'),
    path('Adm/eventos/edit/<int:pk>/', views.evento_edit, name='evento_edit'),
    path('Adm/eventos/delete/<int:pk>/', views.evento_delete, name='evento_delete'),
    path('Adm/eventos/exportar-eventos-csv/', views.exportar_eventos_para_csv, name='exportar_eventos_csv'),

    
    #path carrinho de compras
    path('cart/add/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('cart/ad/<int:produto_id>/', views.adicionar_dentro_carrinho, name='adicionar_dentro_carrinho'),
    path('cart/add/clothes/<int:produto_id>',views.adicionar_roupa_dentro_carrinho, name = 'adicionar_roupa_dentro'),
    path('cart/add/clothe/<int:produto_id>',views.adicionar_roupa, name = 'adicionar_roupa'),
    path('cart/delete/<int:produto_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('cart/delete/clothes/<int:produto_id>/', views.remover_roupa_do_carrinho, name='remover_roupa_carrinho'),
    path('cart/',views.carrinho,name='carrinho'),
    path('store/product/<int:produto_id>',views.produto,name='produto'),
    path('cart/details',views.pessoa_encomenda,name='pessoa_encomenda'),
    path('cart/deleteA/<int:produto_id>',views.remover_dentro_carrinho,name='removerTdentro'),
    
    #path de pagamento
    path('registrar-pagamento/', views.registrar_pagamento, name='registrar_pagamento'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)