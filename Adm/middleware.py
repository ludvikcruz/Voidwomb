from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse

class AdminRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        
        allowed_paths = ['/Adm/users/login/', '/Adm/users/login']  

        # Verifica se o caminho do request está na lista de caminhos permitidos
        if request.path not in allowed_paths and request.path.startswith('/Adm/'):
            if not (request.user.is_authenticated and request.user.is_staff):
                return HttpResponseRedirect(reverse('login'))
        return None


