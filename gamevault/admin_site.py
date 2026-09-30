"""
Admin site customizado para o GameVault.
Substitui o DefaultAdminSite com dashboard de métricas reais.
"""

from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Sum
from django.utils import timezone


class GameVaultAdminSite(AdminSite):
    site_title = "GameVault Admin"
    site_header = "GameVault"
    index_title = "Painel Administrativo"

    def index(self, request, extra_context=None):
        from jogos.models import (
            Avaliacao,
            Conquista,
            Genero,
            ItemListaDesejo,
            Jogo,
            Notificacao,
            Plataforma,
            SessaoJogo,
            StatusJogo,
        )

        jogos_qs = Jogo.objects.all()
        hoje = timezone.localdate()
        este_mes_inicio = hoje.replace(day=1)

        stats = {
            "total_jogos": jogos_qs.count(),
            "total_usuarios": User.objects.count(),
            "total_generos": Genero.objects.count(),
            "total_plataformas": Plataforma.objects.count(),
            "jogando": jogos_qs.filter(status=StatusJogo.PLAYING).count(),
            "concluidos": jogos_qs.filter(
                status__in=[StatusJogo.COMPLETED, StatusJogo.MASTERED]
            ).count(),
            "backlog": jogos_qs.filter(status=StatusJogo.BACKLOG).count(),
            "wishlist_total": ItemListaDesejo.objects.count(),
            "total_horas": jogos_qs.aggregate(s=Sum("horas_jogadas"))["s"] or 0,
            "media_avaliacao": Avaliacao.objects.aggregate(m=Avg("nota"))["m"],
            "total_conquistas": Conquista.objects.count(),
            "conquistas_ok": Conquista.objects.filter(concluida=True).count(),
            "sessoes_mes": SessaoJogo.objects.filter(
                iniciado_em__date__gte=este_mes_inicio
            ).count(),
            "notificacoes_nao_lidas": Notificacao.objects.filter(lida=False).count(),
            "jogos_recentes": jogos_qs.select_related("genero", "usuario").prefetch_related("plataformas").order_by("-criado_em")[:8],
            "top_generos": (
                jogos_qs.values("genero__nome")
                .annotate(total=Count("id"))
                .order_by("-total")[:6]
            ),
            "por_status": (
                jogos_qs.values("status")
                .annotate(total=Count("id"))
                .order_by("-total")
            ),
            "status_labels": dict(StatusJogo.choices),
        }

        extra_context = extra_context or {}
        extra_context.update(stats)
        return super().index(request, extra_context)
