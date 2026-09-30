import json
from decimal import Decimal

from django.db.models import Avg, Count, Max, Min, Sum
from django.db.models.functions import ExtractYear

from .models import Avaliacao, Genero, ItemListaDesejo, Plataforma, StatusJogo


def estatisticas_dashboard(queryset):
    total = queryset.count()
    por_status = dict(
        queryset.values("status")
        .annotate(total=Count("id"))
        .values_list("status", "total")
    )
    horas = queryset.aggregate(s=Sum("horas_jogadas"))["s"] or Decimal("0")

    return {
        "total_jogos": total,
        "jogando": por_status.get(StatusJogo.PLAYING, 0),
        "concluidos": por_status.get(StatusJogo.COMPLETED, 0)
        + por_status.get(StatusJogo.MASTERED, 0),
        "backlog": por_status.get(StatusJogo.BACKLOG, 0),
        "wishlist_status": por_status.get(StatusJogo.WISHLIST, 0),
        "horas_jogadas": horas,
    }


def dados_graficos(queryset, user):
    plataformas = list(
        queryset.values("plataformas__nome")
        .annotate(total=Count("id", distinct=True))
        .order_by("-total")[:8]
    )
    plataformas_labels = [
        p["plataformas__nome"] or "Outra" for p in plataformas
    ]
    plataformas_values = [p["total"] for p in plataformas]

    generos = list(
        queryset.values("genero__nome")
        .annotate(total=Count("id"))
        .order_by("-total")[:8]
    )
    generos_labels = [g["genero__nome"] for g in generos]
    generos_values = [g["total"] for g in generos]

    status_map = dict(StatusJogo.choices)
    status_data = list(
        queryset.values("status").annotate(total=Count("id")).order_by("-total")
    )
    status_labels = [status_map.get(s["status"], s["status"]) for s in status_data]
    status_values = [s["total"] for s in status_data]

    anos = list(
        queryset.annotate(ano=ExtractYear("data_lancamento"))
        .values("ano")
        .annotate(total=Count("id"))
        .order_by("ano")
    )
    anos_labels = [str(a["ano"]) for a in anos if a["ano"]]
    anos_values = [a["total"] for a in anos if a["ano"]]

    avaliacoes = list(
        queryset.exclude(avaliacao_pessoal__isnull=True)
        .values("avaliacao_pessoal")
        .annotate(total=Count("id"))
        .order_by("avaliacao_pessoal")
    )
    rating_labels = [str(int(a["avaliacao_pessoal"])) for a in avaliacoes]
    rating_values = [a["total"] for a in avaliacoes]

    wishlist_count = ItemListaDesejo.objects.filter(usuario=user).count()
    total = queryset.count() or 1
    concluidos = queryset.filter(
        status__in=[StatusJogo.COMPLETED, StatusJogo.MASTERED]
    ).count()
    taxa_conclusao = round((concluidos / total) * 100, 1)

    return {
        "chart_plataformas": json.dumps(
            {"labels": plataformas_labels, "values": plataformas_values}
        ),
        "chart_generos": json.dumps(
            {"labels": generos_labels, "values": generos_values}
        ),
        "chart_status": json.dumps(
            {"labels": status_labels, "values": status_values}
        ),
        "chart_anos": json.dumps({"labels": anos_labels, "values": anos_values}),
        "chart_ratings": json.dumps(
            {"labels": rating_labels, "values": rating_values}
        ),
        "wishlist_count": wishlist_count,
        "taxa_conclusao": taxa_conclusao,
        "media_avaliacao": queryset.aggregate(m=Avg("avaliacao_pessoal"))["m"],
    }


def indicadores_academicos(queryset):
    """Indicadores do dashboard a partir do banco, via ORM."""
    precos = queryset.aggregate(
        media=Avg("preco"),
        maior=Max("preco"),
        menor=Min("preco"),
    )
    avaliacoes = Avaliacao.objects.filter(jogo__in=queryset)
    por_genero = list(
        queryset.values("genero__nome")
        .annotate(total=Count("id"))
        .order_by("-total", "genero__nome")
    )
    por_plataforma = list(
        queryset.values("plataformas__nome")
        .annotate(total=Count("id", distinct=True))
        .order_by("-total", "plataformas__nome")
    )
    return {
        "total_generos": Genero.objects.count(),
        "total_plataformas": Plataforma.objects.count(),
        "total_avaliacoes": avaliacoes.count(),
        "preco_medio": precos["media"],
        "preco_maior": precos["maior"],
        "preco_menor": precos["menor"],
        "media_avaliacoes": avaliacoes.aggregate(m=Avg("nota"))["m"],
        "jogos_por_genero": por_genero,
        "jogos_por_plataforma": por_plataforma,
    }


def recomendacoes_para_usuario(queryset, limite=6):
    favoritos = queryset.exclude(avaliacao_pessoal__isnull=True).order_by(
        "-avaliacao_pessoal"
    )[:3]
    genero_ids = list(favoritos.values_list("genero_id", flat=True))
    if not genero_ids:
        genero_ids = list(queryset.values_list("genero_id", flat=True)[:3])
    if not genero_ids:
        return queryset.none()
    return (
        queryset.filter(genero_id__in=genero_ids)
        .exclude(status__in=[StatusJogo.COMPLETED, StatusJogo.MASTERED])
        .distinct()[:limite]
    )
