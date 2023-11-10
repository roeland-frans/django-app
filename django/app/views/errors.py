from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def error400(request, exception, **kwargs):
    return render(request, "errors/400.html", context={}, status=400)


@requires_csrf_token
def error403(request, exception, **kwargs):
    return render(request, "errors/403.html", context={}, status=403)


@requires_csrf_token
def error404(request, exception, **kwargs):
    return render(request, "errors/404.html", context={}, status=404)


@requires_csrf_token
def error500(request, **kwargs):
    return render(request, "errors/500.html", context={}, status=500)
