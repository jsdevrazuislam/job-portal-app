from django.shortcuts import redirect


def role_verify(func):
    def wrapper_view(request, *args, **kwargs):
        if request.user.role != 'employer':
            return redirect('dashboard')
        return func(request, *args, **kwargs)
    return wrapper_view