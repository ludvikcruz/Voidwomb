from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index')
]