from django.core.exceptions import PermissionDenied
from users.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            if request.user.profile.designation == 'TEACHER':
                return redirect('pdfs:teacher_dashboard')
            else:
                return redirect('pdfs:student_dashboard')   
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                raise PermissionDenied
        return wrapper_func
    return decorator

