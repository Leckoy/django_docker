from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

def role_required(role_name):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role.title != role_name:
                return HttpResponseForbidden("Нет доступа")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
