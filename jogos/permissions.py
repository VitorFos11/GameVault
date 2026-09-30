from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Jogo


def jogos_do_usuario(user):
    if not user.is_authenticated:
        return Jogo.objects.none()
    if user.is_staff:
        return Jogo.objects.all()
    return Jogo.objects.filter(Q(usuario=user) | Q(usuario__isnull=True))


def obter_jogo_usuario(request, jogo_id):
    jogo = get_object_or_404(Jogo, pk=jogo_id)
    if request.user.is_staff:
        return jogo
    if jogo.usuario_id not in (None, request.user.id):
        raise PermissionDenied
    return jogo


def exigir_login(view_func):
    from django.contrib.auth.decorators import login_required

    return login_required(view_func)
