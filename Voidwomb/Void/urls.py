
from django.contrib import admin
from django.urls import include, path
from Void import views
urlpatterns = [
    path('rituals',views.rituals,name = 'rituals'),
    path('about',views.about,name = 'about'),
    path('contact',views.contact,name = 'contact'),
    path('store',views.store,name = 'store'),
 
]
