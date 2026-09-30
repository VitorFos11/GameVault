from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

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
)


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

STATUS_COLORS = {
    StatusJogo.PLAYING:   ("#60a5fa", "▶"),
    StatusJogo.COMPLETED: ("#4ade80", "✓"),
    StatusJogo.MASTERED:  ("#a78bfa", "★"),
    StatusJogo.PAUSED:    ("#facc15", "⏸"),
    StatusJogo.DROPPED:   ("#f87171", "✕"),
    StatusJogo.WISHLIST:  ("#c084fc", "♡"),
    StatusJogo.BACKLOG:   ("#94a3b8", "☐"),
}


def badge_status(jogo):
    color, icon = STATUS_COLORS.get(jogo.status, ("#94a3b8", "?"))
    label = jogo.get_status_display()
    return format_html(
        '<span style="border-radius:99px;padding:2px 10px;font-size:.78rem;font-weight:700;'
        'background:{}22;color:{}">{} {}</span>',
        color, color, icon, label,
    )
badge_status.short_description = "Status"


def capa_thumb(jogo):
    if jogo.capa:
        return format_html(
            '<img src="{}" style="height:48px;width:36px;object-fit:cover;border-radius:4px">',
            jogo.capa.url,
        )
    return "—"
capa_thumb.short_description = "Capa"


# ──────────────────────────────────────────────
# Gênero
# ──────────────────────────────────────────────

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ("nome", "slug", "total_jogos")
    search_fields = ("nome",)
    prepopulated_fields = {"slug": ("nome",)}
    ordering = ("nome",)

    def total_jogos(self, obj):
        c = obj.jogos.count()
        return format_html('<span style="color:#a5b4fc;font-weight:600">{}</span>', c)
    total_jogos.short_description = "Jogos"


# ──────────────────────────────────────────────
# Plataforma
# ──────────────────────────────────────────────

@admin.register(Plataforma)
class PlataformaAdmin(admin.ModelAdmin):
    list_display = ("nome", "slug", "total_jogos", "criado_em")
    search_fields = ("nome",)
    prepopulated_fields = {"slug": ("nome",)}
    readonly_fields = ("criado_em",)
    ordering = ("nome",)

    def total_jogos(self, obj):
        c = obj.jogos.count()
        return format_html('<span style="color:#a5b4fc;font-weight:600">{}</span>', c)
    total_jogos.short_description = "Jogos"


# ──────────────────────────────────────────────
# Jogo
# ──────────────────────────────────────────────

@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = (
        "capa_thumb",
        "nome",
        "usuario",
        "badge_status",
        "plataforma_ref",
        "genero",
        "preco_fmt",
        "horas_jogadas",
        "avaliacao_pessoal",
        "criado_em",
    )
    list_display_links = ("nome",)
    list_filter = ("status", "genero", "plataforma_ref", "multiplayer", "criado_em")
    search_fields = ("nome", "desenvolvedora", "distribuidora", "tags")
    prepopulated_fields = {"slug": ("nome",)}
    readonly_fields = ("criado_em", "atualizado_em", "slug")
    filter_horizontal = ("generos",)
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)
    list_per_page = 25
    actions = ["marcar_concluido", "marcar_jogando", "marcar_backlog"]

    fieldsets = (
        ("Informações básicas", {
            "fields": ("nome", "slug", "descricao", "capa", "banner"),
        }),
        ("Lançamento", {
            "fields": ("data_lancamento", "desenvolvedora", "distribuidora", "website"),
        }),
        ("Classificação", {
            "fields": ("genero", "generos", "plataforma_ref", "plataforma", "classificacao", "multiplayer", "tags"),
        }),
        ("Biblioteca pessoal", {
            "fields": (
                "usuario", "status", "avaliacao_pessoal",
                "preco", "preco_compra",
                "horas_jogadas", "percentual_conclusao", "ultimo_jogado",
            ),
        }),
        ("Metadados", {
            "fields": ("criado_em", "atualizado_em"),
            "classes": ("collapse",),
        }),
    )

    def capa_thumb(self, obj):
        return capa_thumb(obj)
    capa_thumb.short_description = "Capa"

    def badge_status(self, obj):
        return badge_status(obj)
    badge_status.short_description = "Status"

    def preco_fmt(self, obj):
        return format_html("R$ {}", obj.preco)
    preco_fmt.short_description = "Preço"

    @admin.action(description="Marcar como Concluído")
    def marcar_concluido(self, request, queryset):
        updated = queryset.update(status=StatusJogo.COMPLETED)
        self.message_user(request, f"{updated} jogo(s) marcado(s) como Concluído.")

    @admin.action(description="Marcar como Jogando")
    def marcar_jogando(self, request, queryset):
        updated = queryset.update(status=StatusJogo.PLAYING, ultimo_jogado=timezone.now())
        self.message_user(request, f"{updated} jogo(s) marcado(s) como Jogando.")

    @admin.action(description="Mover para Backlog")
    def marcar_backlog(self, request, queryset):
        updated = queryset.update(status=StatusJogo.BACKLOG)
        self.message_user(request, f"{updated} jogo(s) movido(s) para o Backlog.")


# ──────────────────────────────────────────────
# Avaliação
# ──────────────────────────────────────────────

def estrelas(obj):
    cheia = "★" * obj.nota
    vazia = "☆" * (5 - obj.nota)
    return format_html(
        '<span style="color:#eab308;letter-spacing:2px">{}</span>'
        '<span style="color:#334155">{}</span>',
        cheia, vazia,
    )
estrelas.short_description = "Nota"


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("jogo", "usuario", estrelas, "atualizado_em")
    list_filter = ("nota",)
    search_fields = ("jogo__nome", "usuario__username")
    readonly_fields = ("criado_em", "atualizado_em")
    date_hierarchy = "criado_em"


# ──────────────────────────────────────────────
# Wishlist
# ──────────────────────────────────────────────

def badge_prioridade(obj):
    cores = {"low": "#94a3b8", "medium": "#eab308", "high": "#ef4444"}
    cor = cores.get(obj.prioridade, "#94a3b8")
    return format_html(
        '<span style="border-radius:99px;padding:1px 8px;font-size:.76rem;font-weight:700;'
        'background:{}22;color:{}">{}</span>',
        cor, cor, obj.get_prioridade_display(),
    )
badge_prioridade.short_description = "Prioridade"


@admin.register(ItemListaDesejo)
class ItemListaDesejoAdmin(admin.ModelAdmin):
    list_display = ("jogo", "usuario", badge_prioridade, "preco_alvo", "criado_em")
    list_filter = ("prioridade",)
    search_fields = ("jogo__nome", "usuario__username")
    readonly_fields = ("criado_em",)


# ──────────────────────────────────────────────
# Conquistas
# ──────────────────────────────────────────────

@admin.register(Conquista)
class ConquistaAdmin(admin.ModelAdmin):
    list_display = ("nome", "jogo", "badge_concluida", "concluida_em")
    list_filter = ("concluida",)
    search_fields = ("nome", "jogo__nome")

    def badge_concluida(self, obj):
        if obj.concluida:
            return format_html('<span style="color:#4ade80;font-weight:700">✓ Concluída</span>')
        return format_html('<span style="color:#94a3b8">○ Pendente</span>')
    badge_concluida.short_description = "Situação"


# ──────────────────────────────────────────────
# Sessões de jogo
# ──────────────────────────────────────────────

@admin.register(SessaoJogo)
class SessaoJogoAdmin(admin.ModelAdmin):
    list_display = ("jogo", "usuario", "iniciado_em", "duracao_horas")
    list_filter = ("iniciado_em",)
    search_fields = ("jogo__nome", "usuario__username")
    date_hierarchy = "iniciado_em"

    def duracao_horas(self, obj):
        h = obj.duracao_minutos // 60
        m = obj.duracao_minutos % 60
        return f"{h}h {m:02d}m" if h else f"{m}min"
    duracao_horas.short_description = "Duração"


# ──────────────────────────────────────────────
# Notificações
# ──────────────────────────────────────────────

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "usuario", "tipo", "badge_lida", "criado_em")
    list_filter = ("tipo", "lida", "criado_em")
    search_fields = ("titulo", "usuario__username")
    actions = ["marcar_lidas"]
    date_hierarchy = "criado_em"

    def badge_lida(self, obj):
        if obj.lida:
            return format_html('<span style="color:#4ade80">✓ Lida</span>')
        return format_html('<span style="color:#f87171;font-weight:700">• Nova</span>')
    badge_lida.short_description = "Situação"

    @admin.action(description="Marcar como lidas")
    def marcar_lidas(self, request, queryset):
        updated = queryset.update(lida=True)
        self.message_user(request, f"{updated} notificação(ões) marcada(s) como lida.")
