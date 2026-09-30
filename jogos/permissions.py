from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import EntradaBiblioteca, Jogo


MENSAGEM_SEM_PERMISSAO = "Você não possui permissão para acessar esta área."


def exigir_staff(view_func):
    """Somente administradores (is_staff) — catálogo global."""

    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied(MENSAGEM_SEM_PERMISSAO)
        return view_func(request, *args, **kwargs)

    return wrapper


def catalogo_jogos():
    """Jogos do catálogo global (sem dono pessoal no registro Jogo)."""
    return Jogo.objects.filter(usuario__isnull=True)


def biblioteca_entradas(user):
    if not user.is_authenticated:
        return EntradaBiblioteca.objects.none()
    return EntradaBiblioteca.objects.filter(usuario=user)


def jogos_na_biblioteca(user):
    """Jogos que o usuário adicionou à biblioteca pessoal."""
    if not user.is_authenticated:
        return Jogo.objects.none()
    return Jogo.objects.filter(
        entradas_biblioteca__usuario=user,
        usuario__isnull=True,
    ).distinct()


def queryset_dashboard(user):
    """Staff: catálogo global; usuário: biblioteca pessoal."""
    if user.is_staff:
        return catalogo_jogos()
    return jogos_na_biblioteca(user)


def obter_jogo_catalogo(jogo_id):
    return get_object_or_404(catalogo_jogos(), pk=jogo_id)


def obter_entrada_biblioteca(request, jogo_id):
    jogo = obter_jogo_catalogo(jogo_id)
    return get_object_or_404(
        EntradaBiblioteca,
        usuario=request.user,
        jogo=jogo,
    )


def obter_jogo_catalogo_ou_entrada(request, jogo_id):
    """Detalhe: catálogo visível a qualquer logado; retorna (jogo, entrada|None)."""
    jogo = get_object_or_404(
        catalogo_jogos()
        .select_related("genero")
        .prefetch_related("generos", "plataformas"),
        pk=jogo_id,
    )
    entrada = EntradaBiblioteca.objects.filter(
        usuario=request.user, jogo=jogo
    ).first()
    return jogo, entrada
