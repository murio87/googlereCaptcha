from django.shortcuts import redirect


def user_not_authenticated(function=None, redirect_url='home'):
    """"
    """

    def decorator(view_func):
        def wrapper_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)

        return wrapper_view

    if function:
        return decorator(function)
