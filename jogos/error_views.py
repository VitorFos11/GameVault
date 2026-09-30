from django.shortcuts import render


def erro_404(request, exception):
    return render(request, "errors/404.html", status=404)


def erro_403(request, exception):
    return render(request, "errors/403.html", status=403)


def erro_500(request):
    return render(request, "errors/500.html", status=500)
