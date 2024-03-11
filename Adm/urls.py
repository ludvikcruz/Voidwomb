# payment/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('produto/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('produto/editar/<int:id>/', views.editar_produto, name='editar_produto'),
    path('produto/eliminar/<int:id>/', views.eliminar_produto, name='eliminar_produto'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
]