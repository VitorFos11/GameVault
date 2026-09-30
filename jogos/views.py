from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from django.conf import settings

from .forms import (
    AvaliacaoForm,
    BuscaImportacaoForm,
    ConquistaForm,
    ItemListaDesejoForm,
    JogoForm,
    ProgressoJogoForm,
    SessaoJogoForm,
)
from .models import (
    Avaliacao,
    Conquista,
    Genero,
    ItemListaDesejo,
    Jogo,
    Notificacao,
    Plataforma,
    SessaoJogo,
    StatusJogo,
    TipoNotificacao,
)
from .permissions import jogos_do_usuario, obter_jogo_usuario
from .services.game_api import ExternalGameAPIError, get_game_api_service
from .stats import dados_graficos, estatisticas_dashboard, recomendacoes_para_usuario


def landing(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "landing.html")


@login_required
def dashboard(request):
    qs = jogos_do_usuario(request.user).select_related("genero", "plataforma_ref")
    stats = estatisticas_dashboard(qs)
    charts = dados_graficos(qs, request.user)
    recomendados = recomendacoes_para_usuario(qs)
    recentes = qs[:8]
    context = {
        **stats,
        **charts,
        "recomendados": recomendados,
        "recentes": recentes,
    }
    return render(request, "jogos/dashboard.html", context)


def _filtrar_jogos(request, queryset):
    busca = request.GET.get("buscar", "").strip()
    status = request.GET.get("status", "")
    plataforma = request.GET.get("plataforma", "")
    genero = request.GET.get("genero", "")
    ano = request.GET.get("ano", "")
    nota_min = request.GET.get("nota_min", "")
    ordenar = request.GET.get("ordenar", "recente")

    if busca:
        queryset = queryset.filter(
            Q(nome__icontains=busca)
            | Q(desenvolvedora__icontains=busca)
            | Q(distribuidora__icontains=busca)
            | Q(tags__icontains=busca)
            | Q(genero__nome__icontains=busca)
            | Q(plataforma__icontains=busca)
            | Q(plataforma_ref__nome__icontains=busca)
        ).distinct()

    if status:
        queryset = queryset.filter(status=status)
    if plataforma:
        queryset = queryset.filter(
            Q(plataforma_ref__slug=plataforma) | Q(plataforma__iexact=plataforma)
        )
    if genero:
        queryset = queryset.filter(Q(genero__slug=genero) | Q(generos__slug=genero))
    if ano:
        queryset = queryset.filter(data_lancamento__year=ano)
    if nota_min:
        try:
            queryset = queryset.filter(avaliacao_pessoal__gte=float(nota_min))
        except ValueError:
            pass

    ordenacao = {
        "nome": "nome",
        "recente": "-criado_em",
        "lancamento": "-data_lancamento",
        "nota": "-avaliacao_pessoal",
        "horas": "-horas_jogadas",
        "preco": "-preco",
    }.get(ordenar, "-criado_em")
    return queryset.order_by(ordenacao), busca


@login_required
def biblioteca(request):
    qs = jogos_do_usuario(request.user).select_related(
        "genero", "plataforma_ref"
    ).prefetch_related("generos")
    qs, busca = _filtrar_jogos(request, qs)
    view_mode = request.GET.get("view", "grid")

    paginator = Paginator(qs, settings.GAMES_PER_PAGE)
    page = request.GET.get("page")
    jogos = paginator.get_page(page)

    context = {
        "jogos": jogos,
        "busca": busca,
        "view_mode": view_mode,
        "status_choices": StatusJogo.choices,
        "plataformas": Plataforma.objects.all(),
        "generos": Genero.objects.all(),
        "filtros": request.GET,
        "total_filtrado": paginator.count,
    }
    return render(request, "jogos/biblioteca.html", context)


def lista_jogos(request):
    return biblioteca(request)


@login_required
def cadastrar_jogo(request):
    if request.method == "POST":
        form = JogoForm(request.POST, request.FILES)
        if form.is_valid():
            jogo = form.save(commit=False)
            jogo.usuario = request.user
            jogo.save()
            form.save_m2m()
            if not jogo.generos.exists():
                jogo.generos.add(jogo.genero)
            messages.success(request, "Jogo adicionado à sua biblioteca.")
            return redirect("detalhe_jogo", id=jogo.id)
    else:
        form = JogoForm()
    return render(request, "jogos/form.html", {"form": form, "titulo": "Novo jogo"})


@login_required
def editar_jogo(request, id):
    jogo = obter_jogo_usuario(request, id)
    if request.method == "POST":
        form = JogoForm(request.POST, request.FILES, instance=jogo)
        if form.is_valid():
            form.save()
            messages.success(request, "Jogo atualizado com sucesso.")
            return redirect("detalhe_jogo", id=jogo.id)
    else:
        form = JogoForm(instance=jogo)
    return render(
        request, "jogos/form.html", {"form": form, "titulo": "Editar jogo", "jogo": jogo}
    )


@login_required
def excluir_jogo(request, id):
    jogo = obter_jogo_usuario(request, id)
    if request.method == "POST":
        nome = jogo.nome
        jogo.delete()
        messages.success(request, f'Jogo "{nome}" removido.')
        return redirect("biblioteca")
    return render(request, "jogos/excluir.html", {"jogo": jogo})


@login_required
def detalhe_jogo(request, id):
    jogo = get_object_or_404(
        Jogo.objects.select_related("genero", "plataforma_ref", "usuario").prefetch_related(
            "generos", "conquistas", "sessoes", "avaliacoes"
        ),
        pk=id,
    )
    if not request.user.is_staff and jogo.usuario_id not in (
        None,
        request.user.id,
    ):
        raise PermissionDenied

    avaliacao = Avaliacao.objects.filter(jogo=jogo, usuario=request.user).first()
    progresso_form = ProgressoJogoForm(instance=jogo)
    avaliacao_form = AvaliacaoForm(instance=avaliacao)
    conquista_form = ConquistaForm()
    sessao_form = SessaoJogoForm(
        initial={"iniciado_em": timezone.localtime().strftime("%Y-%m-%dT%H:%M")}
    )

    total_conquistas = jogo.conquistas.count()
    conquistas_ok = jogo.conquistas.filter(concluida=True).count()
    pct_conquistas = (
        round((conquistas_ok / total_conquistas) * 100) if total_conquistas else 0
    )

    context = {
        "jogo": jogo,
        "avaliacao": avaliacao,
        "progresso_form": progresso_form,
        "avaliacao_form": avaliacao_form,
        "conquista_form": conquista_form,
        "sessao_form": sessao_form,
        "total_conquistas": total_conquistas,
        "conquistas_ok": conquistas_ok,
        "pct_conquistas": pct_conquistas,
        "na_lista_desejo": ItemListaDesejo.objects.filter(
            usuario=request.user, jogo=jogo
        ).exists(),
        "status_choices": StatusJogo.choices,
    }
    return render(request, "jogos/detalhe.html", context)


@login_required
@require_POST
def atualizar_progresso(request, id):
    jogo = obter_jogo_usuario(request, id)
    form = ProgressoJogoForm(request.POST, instance=jogo)
    if form.is_valid():
        anterior = jogo.status
        jogo = form.save(commit=False)
        jogo.ultimo_jogado = timezone.now()
        jogo.save()
        if (
            anterior != StatusJogo.COMPLETED
            and jogo.status == StatusJogo.COMPLETED
        ):
            Notificacao.objects.create(
                usuario=request.user,
                tipo=TipoNotificacao.JOGO_CONCLUIDO,
                titulo="Jogo concluído!",
                mensagem=f'Você concluiu "{jogo.nome}".',
            )
        messages.success(request, "Progresso atualizado.")
    else:
        messages.error(request, "Não foi possível atualizar o progresso.")
    return redirect("detalhe_jogo", id=id)


@login_required
@require_POST
def salvar_avaliacao(request, id):
    jogo = obter_jogo_usuario(request, id)
    avaliacao = Avaliacao.objects.filter(jogo=jogo, usuario=request.user).first()
    form = AvaliacaoForm(request.POST, instance=avaliacao)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.jogo = jogo
        obj.usuario = request.user
        obj.save()
        jogo.avaliacao_pessoal = obj.nota
        jogo.save(update_fields=["avaliacao_pessoal"])
        messages.success(request, "Avaliação salva.")
    else:
        messages.error(request, "Verifique a nota (1 a 5).")
    return redirect("detalhe_jogo", id=id)


@login_required
@require_POST
def alterar_status_rapido(request, id):
    jogo = obter_jogo_usuario(request, id)
    status = request.POST.get("status")
    if status in dict(StatusJogo.choices):
        jogo.status = status
        jogo.save(update_fields=["status", "atualizado_em"])
        messages.success(request, "Status atualizado.")
    return redirect("detalhe_jogo", id=id)


@login_required
def lista_desejos(request):
    itens = (
        ItemListaDesejo.objects.filter(usuario=request.user)
        .select_related("jogo", "jogo__genero", "jogo__plataforma_ref")
        .order_by("-prioridade", "-criado_em")
    )
    return render(request, "jogos/lista_desejos.html", {"itens": itens})


@login_required
@require_POST
def adicionar_lista_desejo(request, id):
    jogo = obter_jogo_usuario(request, id)
    ItemListaDesejo.objects.get_or_create(usuario=request.user, jogo=jogo)
    jogo.status = StatusJogo.WISHLIST
    jogo.save(update_fields=["status"])
    messages.success(request, "Adicionado à lista de desejos.")
    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)
    return redirect("detalhe_jogo", id=id)


@login_required
@require_POST
def remover_lista_desejo(request, id):
    jogo = obter_jogo_usuario(request, id)
    ItemListaDesejo.objects.filter(usuario=request.user, jogo=jogo).delete()
    messages.success(request, "Removido da lista de desejos.")
    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)
    return redirect("lista_desejos")


@login_required
def editar_item_desejo(request, item_id):
    item = get_object_or_404(ItemListaDesejo, pk=item_id, usuario=request.user)
    if request.method == "POST":
        form = ItemListaDesejoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item da wishlist atualizado.")
            return redirect("lista_desejos")
    else:
        form = ItemListaDesejoForm(instance=item)
    return render(
        request,
        "jogos/item_desejo_form.html",
        {"form": form, "item": item},
    )


@login_required
def conquistas_view(request):
    jogos = jogos_do_usuario(request.user).prefetch_related("conquistas")
    return render(request, "jogos/conquistas.html", {"jogos": jogos})


@login_required
@require_POST
def adicionar_conquista(request, id):
    jogo = obter_jogo_usuario(request, id)
    form = ConquistaForm(request.POST)
    if form.is_valid():
        c = form.save(commit=False)
        c.jogo = jogo
        if c.concluida and not c.concluida_em:
            c.concluida_em = timezone.now()
        c.save()
        if c.concluida:
            Notificacao.objects.create(
                usuario=request.user,
                tipo=TipoNotificacao.CONQUISTA,
                titulo="Conquista desbloqueada",
                mensagem=f"{c.nome} em {jogo.nome}",
            )
        messages.success(request, "Conquista adicionada.")
    return redirect("detalhe_jogo", id=id)


@login_required
@require_POST
def registrar_sessao(request, id):
    jogo = obter_jogo_usuario(request, id)
    form = SessaoJogoForm(request.POST)
    if form.is_valid():
        sessao = form.save(commit=False)
        sessao.jogo = jogo
        sessao.usuario = request.user
        sessao.save()
        horas = sessao.duracao_minutos / 60
        jogo.horas_jogadas += horas
        jogo.ultimo_jogado = timezone.now()
        jogo.save(update_fields=["horas_jogadas", "ultimo_jogado"])
        messages.success(request, "Sessão registrada.")
    else:
        messages.error(request, "Dados da sessão inválidos.")
    return redirect("detalhe_jogo", id=id)


@login_required
def estatisticas_view(request):
    qs = jogos_do_usuario(request.user)
    charts = dados_graficos(qs, request.user)
    stats = estatisticas_dashboard(qs)
    return render(
        request,
        "jogos/estatisticas.html",
        {**stats, **charts},
    )


@login_required
def configuracoes(request):
    return render(request, "jogos/configuracoes.html")


@login_required
def notificacoes_view(request):
    nots = request.user.notificacoes.all()[:50]
    request.user.notificacoes.filter(lida=False).update(lida=True)
    return render(request, "jogos/notificacoes.html", {"notificacoes": nots})


@login_required
def importar_jogo_api(request):
    service = get_game_api_service()
    resultados = []
    form = BuscaImportacaoForm(request.GET or None)
    if form.is_valid() and form.cleaned_data["q"]:
        try:
            resultados = service.search(form.cleaned_data["q"])
        except ExternalGameAPIError as exc:
            messages.error(request, str(exc))
    return render(
        request,
        "jogos/importar_api.html",
        {"form": form, "resultados": resultados, "api_enabled": service.enabled},
    )

