# payment/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.adm,name='admin'),
    #Paths dos produtos
    path('produtos/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('produtos/editar/<int:id>/', views.editar_produto, name='editar_produto'),
    path('produtos/eliminar/<int:id>/', views.eliminar_produto, name='eliminar_produto'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produtos/importExcel/', views.lista_produtos, name='upload_excel'),
    path('produtos/ExportExel/', views.exportar_produtos_csv, name='exportar_produtos'),
    path('caminho/para/eliminar/produtos/selecionados/', views.eliminar_selecionados, name='eliminar_produtos_selecionados'),
    #Paths dos users
    path('users/login',views.login_view,name ='login'),
    path('users/logout',views.logout_view,name ='logout'),
    
    #path paises
    path('paises/', views.listar_paises, name='listar_paises'),
    path('paises/adicionar',views.paises_adicionar,name ='adicionar_paises'),
    path('paises/editar/<int:id>/', views.editar_pais, name='editar_pais'),
    path('paises/excluir/<int:id>/', views.excluir_pais, name='excluir_pais'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)