# payment/urls.py
from django.urls import path
from payment import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('registrar-pagamento/', views.registrar_pagamento, name='registrar_pagamento'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)