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
    
    #Paths dos users
    path('users/login',views.login_view,name ='login'),
    path('users/logout',views.logout_view,name ='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)