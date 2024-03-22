# payment/urls.py
#git clone -b t https://github.com/ludvikcruz/Voidwomb.git

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
    path('produtos/', views.lista_produtos_tamanhos, name='lista_produtos'),
    path('produtos/importExcel/', views.lista_produtos_tamanhos, name='upload_excel'),
    path('produtos/ExportExel/', views.exportar_produtos_csv, name='exportar_produtos'),
    path('caminho/para/eliminar/produtos/selecionados/', views.eliminar_selecionados, name='eliminar_produtos_selecionados'),
    
    path("produtos/tamanhos/adicionar", views.adicionar_tamanho, name="adicionar_tamanho"),
    path('produtos/tamanho/editar/<int:id>/', views.editar_tamanho, name='editar_tamanho'),
    path('produtos/tamanho/excluir/<int:id>/', views.excluir_tamanho, name='excluir_tamanho'),
    
    #Paths dos users
    path('users/login',views.login_view,name ='login'),
    path('users/logout',views.logout_view,name ='logout'),
    
    #path paises
    path('paises/', views.listar_paises, name='listar_paises'),
    path('paises/adicionar',views.paises_adicionar,name ='adicionar_paises'),
    path('paises/editar/<int:id>/', views.editar_pais, name='editar_pais'),
    path('paises/excluir/<int:id>/', views.excluir_pais, name='excluir_pais'),
    path('paises/import-countries/', views.listar_paises, name='import_countries'),

    #paths dos eventos
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/add/', views.evento_add, name='evento_add'),
    path('eventos/edit/<int:pk>/', views.evento_edit, name='evento_edit'),
    path('eventos/delete/<int:pk>/', views.evento_delete, name='evento_delete'),
    path('eventos/exportar-eventos-csv/', views.exportar_eventos_para_csv, name='exportar_eventos_csv'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)