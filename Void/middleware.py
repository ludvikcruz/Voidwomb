# middleware.py no seu app
from django.http import HttpResponseNotFound
from django.template.loader import render_to_string

<<<<<<< HEAD
# class Custom404Middleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         if response.status_code == 404:
#             return HttpResponseNotFound(render_to_string('404.html', request=request))
#         return response

# class Custom500Middleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         if response.status_code == 500:
#             return HttpResponseNotFound(render_to_string('500.html', request=request))
#         return response
=======
#class Custom404Middleware:
 #   def __init__(self, get_response):
  #      self.get_response = get_response

#    def __call__(self, request):
 #       response = self.get_response(request)
  #      if response.status_code == 404:
   #         return HttpResponseNotFound(render_to_string('404.html', request=request))
    #    return response

#class Custom500Middleware:
 #   def __init__(self, get_response):
  #      self.get_response = get_response
#
 #   def __call__(self, request):
  #      response = self.get_response(request)
   #     if response.status_code == 500:
    #        return HttpResponseNotFound(render_to_string('500.html', request=request))
     #   return response
>>>>>>> c06c20a (abash: line 3: \: command not found)
