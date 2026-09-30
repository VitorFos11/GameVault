from django.contrib import admin

from .models import (
    Avaliacao,
    Conquista,
    Genero,
    ItemListaDesejo,
    Jogo,
    Notificacao,
    Plataforma,
    SessaoJogo,
)


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ("nome", "slug")
    search_fields = ("nome",)
    prepopulated_fields = {"slug": ("nome",)}


@admin.register(Plataforma)
class PlataformaAdmin(admin.ModelAdmin):
    list_display = ("nome", "slug", "criado_em")
    search_fields = ("nome",)
    prepopulated_fields = {"slug": ("nome",)}


@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "usuario",
        "status",
        "plataforma_ref",
        "genero",
        "preco",
        "horas_jogadas",
    )
    list_filter = ("status", "genero", "plataforma_ref", "multiplayer")
    search_fields = ("nome", "desenvolvedora", "distribuidora")
    prepopulated_fields = {"slug": ("nome",)}
    readonly_fields = ("criado_em", "atualizado_em")
    filter_horizontal = ("generos",)


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("jogo", "usuario", "nota", "atualizado_em")
    list_filter = ("nota",)


@admin.register(ItemListaDesejo)
class ItemListaDesejoAdmin(admin.ModelAdmin):
    list_display = ("jogo", "usuario", "prioridade", "preco_alvo")
    list_filter = ("prioridade",)


@admin.register(Conquista)
class ConquistaAdmin(admin.ModelAdmin):
    list_display = ("nome", "jogo", "concluida", "concluida_em")
    list_filter = ("concluida",)


@admin.register(SessaoJogo)
class SessaoJogoAdmin(admin.ModelAdmin):
    list_display = ("jogo", "usuario", "iniciado_em", "duracao_minutos")
    list_filter = ("iniciado_em",)


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "usuario", "tipo", "lida", "criado_em")
    list_filter = ("tipo", "lida")
