from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Avg, Count
from django.shortcuts import redirect, render

from jogos.permissions import jogos_do_usuario
from jogos.stats import estatisticas_dashboard

from .forms import PerfilForm, RegistroForm


class GameVaultLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class GameVaultLogoutView(LogoutView):
    next_page = "landing"


def registro(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Conta criada. Bem-vindo ao GameVault!")
            return redirect("dashboard")
    else:
        form = RegistroForm()
    return render(request, "accounts/registro.html", {"form": form})


@login_required
def perfil(request):
    perfil_obj = request.user.perfil
    qs = jogos_do_usuario(request.user)
    stats = estatisticas_dashboard(qs)
    generos_fav = (
        qs.values("genero__nome")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )
    plataformas_fav = (
        qs.values("plataformas__nome")
        .annotate(total=Count("id", distinct=True))
        .order_by("-total")[:5]
    )
    media = qs.aggregate(m=Avg("avaliacao_pessoal"))["m"]

    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES, instance=perfil_obj, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado.")
            return redirect("accounts:perfil")
    else:
        form = PerfilForm(instance=perfil_obj, user=request.user)

    context = {
        "form": form,
        "stats": stats,
        "generos_fav": generos_fav,
        "plataformas_fav": plataformas_fav,
        "media_avaliacao": media,
        "member_since": request.user.date_joined,
    }
    return render(request, "accounts/perfil.html", context)
