# payment/urls.py
from django.urls import path
from payment import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('create/', views.create_payment, name='create_payment'),
    path('execute/', views.execute_payment, name='execute_payment'),
    path('cancel/', views.payment_cancelled, name='cancel_payment'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)