from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from django.conf import settings

from .forms import (
    AvaliacaoForm,
    ConquistaForm,
    GeneroForm,
    ItemListaDesejoForm,
    JogoForm,
    PlataformaForm,
    ProgressoJogoForm,
    SessaoJogoForm,
)
from .models import (
    Avaliacao,
    Conquista,
    EntradaBiblioteca,
    Genero,
    ItemListaDesejo,
    Jogo,
    Notificacao,
    Plataforma,
    SessaoJogo,
    StatusJogo,
    TipoNotificacao,
)
from .permissions import (
    biblioteca_entradas,
    catalogo_jogos,
    exigir_staff,
    jogos_na_biblioteca,
    obter_entrada_biblioteca,
    obter_jogo_catalogo,
    obter_jogo_catalogo_ou_entrada,
    queryset_dashboard,
)
from .stats import (
    dados_graficos,
    dados_graficos_entradas,
    estatisticas_dashboard,
    estatisticas_dashboard_entradas,
    indicadores_academicos,
    recomendacoes_para_usuario,
)


def _redirect_seguro(request, destino, *, fallback, **kwargs):
    """Só aceita 'next' que aponte para o próprio site."""
    if destino and url_has_allowed_host_and_scheme(
        destino, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return redirect(destino)
    return redirect(fallback, **kwargs)


def landing(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "landing.html")


@login_required
def dashboard(request):
    global_view = request.user.is_staff
    if global_view:
        qs = queryset_dashboard(request.user).select_related("genero").prefetch_related(
            "plataformas"
        )
        context = {
            "dashboard_global": True,
            **estatisticas_dashboard(qs),
            **indicadores_academicos(qs, global_catalogo=True),
            "recomendados": recomendacoes_para_usuario(qs)[:6],
            "recentes": qs[:8],
        }
    else:
        entradas = biblioteca_entradas(request.user).select_related(
            "jogo", "jogo__genero"
        ).prefetch_related("jogo__plataformas")
        qs = jogos_na_biblioteca(request.user).select_related("genero").prefetch_related(
            "plataformas"
        )
        context = {
            "dashboard_global": False,
            **estatisticas_dashboard_entradas(entradas),
            **indicadores_academicos(qs, global_catalogo=False),
            "recomendados": recomendacoes_para_usuario(qs, entradas=entradas),
            "recentes": qs[:8],
            "entradas_recentes": entradas[:8],
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
            | Q(plataformas__nome__icontains=busca)
        ).distinct()

    if status:
        queryset = queryset.filter(status=status)
    if plataforma:
        queryset = queryset.filter(plataformas__slug=plataforma).distinct()
    if genero:
        queryset = queryset.filter(
            Q(genero__slug=genero) | Q(generos__slug=genero)
        ).distinct()
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


def _filtrar_entradas(request, entradas):
    busca = request.GET.get("buscar", "").strip()
    status = request.GET.get("status", "")
    plataforma = request.GET.get("plataforma", "")
    genero = request.GET.get("genero", "")
    ano = request.GET.get("ano", "")
    nota_min = request.GET.get("nota_min", "")
    ordenar = request.GET.get("ordenar", "recente")

    if busca:
        entradas = entradas.filter(
            Q(jogo__nome__icontains=busca)
            | Q(jogo__desenvolvedora__icontains=busca)
            | Q(jogo__distribuidora__icontains=busca)
            | Q(jogo__tags__icontains=busca)
            | Q(jogo__genero__nome__icontains=busca)
            | Q(jogo__plataformas__nome__icontains=busca)
        ).distinct()

    if status:
        entradas = entradas.filter(status=status)
    if plataforma:
        entradas = entradas.filter(jogo__plataformas__slug=plataforma).distinct()
    if genero:
        entradas = entradas.filter(
            Q(jogo__genero__slug=genero) | Q(jogo__generos__slug=genero)
        ).distinct()
    if ano:
        entradas = entradas.filter(jogo__data_lancamento__year=ano)
    if nota_min:
        try:
            entradas = entradas.filter(avaliacao_pessoal__gte=float(nota_min))
        except ValueError:
            pass

    ordenacao = {
        "nome": "jogo__nome",
        "recente": "-adicionado_em",
        "lancamento": "-jogo__data_lancamento",
        "nota": "-avaliacao_pessoal",
        "horas": "-horas_jogadas",
        "preco": "-jogo__preco",
    }.get(ordenar, "-adicionado_em")
    return entradas.order_by(ordenacao), busca


@login_required
def biblioteca(request):
    qs = biblioteca_entradas(request.user).select_related(
        "jogo", "jogo__genero"
    ).prefetch_related("jogo__generos", "jogo__plataformas")
    qs, busca = _filtrar_entradas(request, qs)
    view_mode = request.GET.get("view", "grid")

    paginator = Paginator(qs, settings.GAMES_PER_PAGE)
    page = request.GET.get("page")
    entradas = paginator.get_page(page)

    context = {
        "entradas": entradas,
        "busca": busca,
        "view_mode": view_mode,
        "status_choices": StatusJogo.choices,
        "plataformas": Plataforma.objects.all(),
        "generos": Genero.objects.all(),
        "filtros": request.GET,
        "total_filtrado": paginator.count,
    }
    return render(request, "jogos/biblioteca.html", context)


@login_required
def explorar_jogos(request):
    qs = catalogo_jogos().select_related("genero").prefetch_related(
        "generos", "plataformas"
    )
    qs, busca = _filtrar_jogos(request, qs)
    ids_na_biblioteca = set(
        biblioteca_entradas(request.user).values_list("jogo_id", flat=True)
    )
    paginator = Paginator(qs, settings.GAMES_PER_PAGE)
    page = request.GET.get("page")
    jogos = paginator.get_page(page)

    context = {
        "jogos": jogos,
        "busca": busca,
        "ids_na_biblioteca": ids_na_biblioteca,
        "status_choices": StatusJogo.choices,
        "plataformas": Plataforma.objects.all(),
        "generos": Genero.objects.all(),
        "filtros": request.GET,
        "total_filtrado": paginator.count,
    }
    return render(request, "jogos/explorar.html", context)


def lista_jogos(request):
    return biblioteca(request)


@exigir_staff
def cadastrar_jogo(request):
    if request.method == "POST":
        form = JogoForm(request.POST, request.FILES)
        if form.is_valid():
            jogo = form.save(commit=False)
            jogo.usuario = None
            jogo.save()
            form.save_m2m()
            if jogo.genero_id:
                jogo.generos.add(jogo.genero)
            messages.success(request, "Jogo adicionado ao catálogo global.")
            return redirect("detalhe_jogo", id=jogo.id)
    else:
        form = JogoForm()
    return render(request, "jogos/form.html", {"form": form, "titulo": "Novo jogo"})


@exigir_staff
def editar_jogo(request, id):
    jogo = obter_jogo_catalogo(id)
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


@exigir_staff
def excluir_jogo(request, id):
    jogo = obter_jogo_catalogo(id)
    if request.method == "POST":
        nome = jogo.nome
        jogo.delete()
        messages.success(request, f'Jogo "{nome}" removido.')
        return redirect("biblioteca")
    return render(request, "jogos/excluir.html", {"jogo": jogo})


@login_required
def detalhe_jogo(request, id):
    jogo, entrada = obter_jogo_catalogo_ou_entrada(request, id)
    jogo = (
        catalogo_jogos()
        .select_related("genero")
        .prefetch_related("generos", "plataformas", "avaliacoes")
        .get(pk=jogo.pk)
    )

    avaliacao = Avaliacao.objects.filter(jogo=jogo, usuario=request.user).first()
    progresso_form = (
        ProgressoJogoForm(instance=entrada) if entrada else None
    )
    avaliacao_form = AvaliacaoForm(instance=avaliacao)
    conquista_form = ConquistaForm()
    sessao_form = SessaoJogoForm(
        initial={"iniciado_em": timezone.localtime().strftime("%Y-%m-%dT%H:%M")}
    )

    media_notas = jogo.avaliacoes.aggregate(m=Avg("nota"))["m"]

    conquistas_qs = Conquista.objects.filter(jogo=jogo, usuario=request.user)
    total_conquistas = conquistas_qs.count()
    conquistas_ok = conquistas_qs.filter(concluida=True).count()
    pct_conquistas = (
        round((conquistas_ok / total_conquistas) * 100) if total_conquistas else 0
    )

    status_exibicao = entrada.status if entrada else StatusJogo.BACKLOG
    context = {
        "jogo": jogo,
        "entrada": entrada,
        "status_exibicao": status_exibicao,
        "avaliacao": avaliacao,
        "progresso_form": progresso_form,
        "conquistas": conquistas_qs,
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
        "media_notas": media_notas,
        "avaliacoes": jogo.avaliacoes.select_related("usuario"),
    }
    return render(request, "jogos/detalhe.html", context)


@login_required
@require_POST
def adicionar_biblioteca(request, id):
    jogo = obter_jogo_catalogo(id)
    entrada, created = EntradaBiblioteca.objects.get_or_create(
        usuario=request.user,
        jogo=jogo,
        defaults={"status": StatusJogo.BACKLOG},
    )
    if created:
        messages.success(request, f'"{jogo.nome}" adicionado à sua biblioteca.')
    else:
        messages.info(request, "Este jogo já está na sua biblioteca.")
    return _redirect_seguro(
        request, request.POST.get("next"), fallback="detalhe_jogo", id=id
    )


@login_required
@require_POST
def atualizar_progresso(request, id):
    jogo, entrada = obter_jogo_catalogo_ou_entrada(request, id)
    if not entrada:
        messages.error(request, "Adicione o jogo à biblioteca para registrar progresso.")
        return redirect("detalhe_jogo", id=id)
    form = ProgressoJogoForm(request.POST, instance=entrada)
    if form.is_valid():
        anterior = entrada.status
        entrada = form.save(commit=False)
        entrada.ultimo_jogado = timezone.now()
        entrada.save()
        if (
            anterior != StatusJogo.COMPLETED
            and entrada.status == StatusJogo.COMPLETED
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
    jogo, entrada = obter_jogo_catalogo_ou_entrada(request, id)
    if not entrada:
        messages.error(request, "Adicione o jogo à biblioteca para avaliar.")
        return redirect("detalhe_jogo", id=id)
    avaliacao = Avaliacao.objects.filter(jogo=jogo, usuario=request.user).first()
    form = AvaliacaoForm(request.POST, instance=avaliacao)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.jogo = jogo
        obj.usuario = request.user
        obj.save()
        entrada.avaliacao_pessoal = obj.nota
        entrada.save(update_fields=["avaliacao_pessoal", "atualizado_em"])
        messages.success(request, "Avaliação salva.")
    else:
        messages.error(request, "Verifique a nota (1 a 5).")
    return redirect("detalhe_jogo", id=id)


@login_required
@require_POST
def excluir_avaliacao(request, id):
    jogo, entrada = obter_jogo_catalogo_ou_entrada(request, id)
    if not entrada:
        return redirect("detalhe_jogo", id=id)
    Avaliacao.objects.filter(jogo=jogo, usuario=request.user).delete()
    entrada.avaliacao_pessoal = None
    entrada.save(update_fields=["avaliacao_pessoal", "atualizado_em"])
    messages.success(request, "Avaliação removida.")
    return redirect("detalhe_jogo", id=id)


@login_required
def lista_generos(request):
    generos = Genero.objects.annotate(total_jogos=Count("jogos"))
    return render(
        request,
        "jogos/catalogo_lista.html",
        {
            "titulo": "Gêneros",
            "subtitulo": "Um gênero pode estar ligado a vários jogos (1:N).",
            "itens": generos,
            "criar_url": "cadastrar_genero",
            "criar_label": "Novo gênero",
            "editar_url": "editar_genero",
            "excluir_url": "excluir_genero",
            "campo_extra": "descricao",
            "pode_gerenciar": request.user.is_staff,
        },
    )


@exigir_staff
def cadastrar_genero(request):
    return _salvar_catalogo(
        request,
        GeneroForm,
        "Novo gênero",
        "Informe o nome do gênero. Depois ele poderá ser escolhido ao cadastrar um jogo.",
        "lista_generos",
        "Gênero cadastrado.",
    )


@exigir_staff
def editar_genero(request, id):
    genero = get_object_or_404(Genero, pk=id)
    return _salvar_catalogo(
        request,
        GeneroForm,
        "Editar gênero",
        f"{genero.jogos.count()} jogo(s) usam este gênero.",
        "lista_generos",
        "Gênero atualizado.",
        instance=genero,
    )


@exigir_staff
def excluir_genero(request, id):
    genero = get_object_or_404(Genero, pk=id)
    return _excluir_catalogo(
        request,
        genero,
        "Excluir gênero?",
        "lista_generos",
        f'Gênero "{genero.nome}" removido.',
        "Não é possível excluir este gênero porque existem jogos vinculados a ele.",
    )


@login_required
def lista_plataformas(request):
    plataformas = Plataforma.objects.annotate(total_jogos=Count("jogos"))
    return render(
        request,
        "jogos/catalogo_lista.html",
        {
            "titulo": "Plataformas",
            "subtitulo": "Cada plataforma é separada e pode estar ligada a vários jogos (N:N).",
            "itens": plataformas,
            "criar_url": "cadastrar_plataforma",
            "criar_label": "Nova plataforma",
            "editar_url": "editar_plataforma",
            "excluir_url": "excluir_plataforma",
            "campo_extra": "fabricante",
            "pode_gerenciar": request.user.is_staff,
        },
    )


@exigir_staff
def cadastrar_plataforma(request):
    return _salvar_catalogo(
        request,
        PlataformaForm,
        "Nova plataforma",
        "Cadastre a plataforma antes de associá-la a um jogo.",
        "lista_plataformas",
        "Plataforma cadastrada.",
    )


@exigir_staff
def editar_plataforma(request, id):
    plataforma = get_object_or_404(Plataforma, pk=id)
    return _salvar_catalogo(
        request,
        PlataformaForm,
        "Editar plataforma",
        f"{plataforma.jogos.count()} jogo(s) usam esta plataforma.",
        "lista_plataformas",
        "Plataforma atualizada.",
        instance=plataforma,
    )


@exigir_staff
def excluir_plataforma(request, id):
    plataforma = get_object_or_404(Plataforma, pk=id)
    if request.method == "POST" and plataforma.jogos.exists():
        messages.error(
            request,
            "Não é possível excluir esta plataforma porque existem jogos vinculados a ela.",
        )
        return redirect("lista_plataformas")
    return _excluir_catalogo(
        request,
        plataforma,
        "Excluir plataforma?",
        "lista_plataformas",
        f'Plataforma "{plataforma.nome}" removida.',
        "Não é possível excluir esta plataforma porque existem jogos vinculados a ela.",
    )


def _salvar_catalogo(request, form_class, titulo, subtitulo, redirect_name, sucesso, instance=None):
    if request.method == "POST":
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, sucesso)
            return redirect(redirect_name)
    else:
        form = form_class(instance=instance)
    return render(
        request,
        "jogos/catalogo_form.html",
        {
            "form": form,
            "titulo": titulo,
            "subtitulo": subtitulo,
            "voltar_url": redirect_name,
        },
    )


def _excluir_catalogo(request, objeto, titulo, redirect_name, sucesso, bloqueio):
    if request.method == "POST":
        try:
            objeto.delete()
        except ProtectedError:
            messages.error(request, bloqueio)
            return redirect(redirect_name)
        messages.success(request, sucesso)
        return redirect(redirect_name)
    return render(
        request,
        "jogos/catalogo_excluir.html",
        {
            "titulo": titulo,
            "objeto": objeto,
            "voltar_url": redirect_name,
            "aviso": bloqueio,
        },
    )


@login_required
@require_POST
def alterar_status_rapido(request, id):
    jogo, entrada = obter_jogo_catalogo_ou_entrada(request, id)
    if not entrada:
        messages.error(request, "Adicione o jogo à biblioteca para alterar o status.")
        return redirect("detalhe_jogo", id=id)
    status = request.POST.get("status")
    if status in dict(StatusJogo.choices):
        entrada.status = status
        entrada.save(update_fields=["status", "atualizado_em"])
        messages.success(request, "Status atualizado.")
    return redirect("detalhe_jogo", id=id)


@login_required
def lista_desejos(request):
    itens = (
        ItemListaDesejo.objects.filter(usuario=request.user)
        .select_related("jogo", "jogo__genero")
        .prefetch_related("jogo__plataformas")
        .order_by("-prioridade", "-criado_em")
    )
    return render(request, "jogos/lista_desejos.html", {"itens": itens})


@login_required
@require_POST
def adicionar_lista_desejo(request, id):
    jogo = obter_jogo_catalogo(id)
    ItemListaDesejo.objects.get_or_create(usuario=request.user, jogo=jogo)
    entrada = EntradaBiblioteca.objects.filter(
        usuario=request.user, jogo=jogo
    ).first()
    if entrada:
        entrada.status = StatusJogo.WISHLIST
        entrada.save(update_fields=["status", "atualizado_em"])
    messages.success(request, "Adicionado à lista de desejos.")
    return _redirect_seguro(
        request, request.POST.get("next"), fallback="detalhe_jogo", id=id
    )


@login_required
@require_POST
def remover_lista_desejo(request, id):
    jogo = obter_jogo_catalogo(id)
    ItemListaDesejo.objects.filter(usuario=request.user, jogo=jogo).delete()
    messages.success(request, "Removido da lista de desejos.")
    return _redirect_seguro(
        request, request.POST.get("next"), fallback="lista_desejos"
    )


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
    from django.db.models import Prefetch

    entradas = (
        biblioteca_entradas(request.user)
        .select_related("jogo")
        .prefetch_related(
            Prefetch(
                "jogo__conquistas",
                queryset=Conquista.objects.filter(usuario=request.user),
            )
        )
    )
    return render(request, "jogos/conquistas.html", {"entradas": entradas})


@login_required
@require_POST
def adicionar_conquista(request, id):
    jogo, entrada = obter_jogo_catalogo_ou_entrada(request, id)
    if not entrada:
        messages.error(request, "Adicione o jogo à biblioteca para registrar conquistas.")
        return redirect("detalhe_jogo", id=id)
    form = ConquistaForm(request.POST)
    if form.is_valid():
        c = form.save(commit=False)
        c.jogo = jogo
        c.usuario = request.user
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
    jogo, entrada = obter_jogo_catalogo_ou_entrada(request, id)
    if not entrada:
        messages.error(request, "Adicione o jogo à biblioteca para registrar sessões.")
        return redirect("detalhe_jogo", id=id)
    form = SessaoJogoForm(request.POST)
    if form.is_valid():
        sessao = form.save(commit=False)
        sessao.jogo = jogo
        sessao.usuario = request.user
        sessao.save()
        horas = sessao.duracao_minutos / 60
        entrada.horas_jogadas += horas
        entrada.ultimo_jogado = timezone.now()
        entrada.save(update_fields=["horas_jogadas", "ultimo_jogado", "atualizado_em"])
        messages.success(request, "Sessão registrada.")
    else:
        messages.error(request, "Dados da sessão inválidos.")
    return redirect("detalhe_jogo", id=id)


@login_required
def estatisticas_view(request):
    if request.user.is_staff:
        qs = catalogo_jogos()
        charts = dados_graficos(qs, request.user)
        stats = estatisticas_dashboard(qs)
    else:
        entradas = biblioteca_entradas(request.user)
        qs = jogos_na_biblioteca(request.user)
        charts = dados_graficos_entradas(entradas, request.user)
        stats = estatisticas_dashboard_entradas(entradas)
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

