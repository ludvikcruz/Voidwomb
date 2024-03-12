# payment/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.adm,name='admin'),
    path('produto/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('produto/editar/<int:id>/', views.editar_produto, name='editar_produto'),
    path('produto/eliminar/<int:id>/', views.eliminar_produto, name='eliminar_produto'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('upload-excel/', views.upload_excel_view, name='upload_excel'),
    path('users/login',views.login_view,name ='login'),
    path('users/register',views.register_view,name ='register'),
    path('users/logout',views.register_view,name ='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)