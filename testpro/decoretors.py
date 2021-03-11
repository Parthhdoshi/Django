from django.http import HttpResponse
from django.shortcuts import redirect
from . import views
from .views import *

def unauth_user(view_fun):
    def wrapper_fun(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('ads')
        else:
            return view_fun(request, *args, **kwargs)

    return wrapper_fun

def allowed_user(allowed_roles=[]):
    def decoretors(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            group=None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('userpage')
        return wrapper_func
    return decoretors


# def admin_only(view_func):
#     def wrapper_function(request, *args, **kwargs):
#         group = None
#         if request.user.groups.exists():
#             group = request.user.groups.all()[0].name

#         if group == 'customer':
#             return redirect ('user')

#         if group == 'admin':
#             return view_func(request, *args, **kwargs)
#     return wrapper_function


