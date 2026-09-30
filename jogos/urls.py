from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("biblioteca/", views.biblioteca, name="biblioteca"),
    path("novo/", views.cadastrar_jogo, name="cadastrar_jogo"),
    path("jogo/<int:id>/", views.detalhe_jogo, name="detalhe_jogo"),
    path("editar/<int:id>/", views.editar_jogo, name="editar_jogo"),
    path("excluir/<int:id>/", views.excluir_jogo, name="excluir_jogo"),
    path("jogo/<int:id>/progresso/", views.atualizar_progresso, name="atualizar_progresso"),
    path("jogo/<int:id>/avaliacao/", views.salvar_avaliacao, name="salvar_avaliacao"),
    path("jogo/<int:id>/avaliacao/excluir/", views.excluir_avaliacao, name="excluir_avaliacao"),
    path("generos/", views.lista_generos, name="lista_generos"),
    path("generos/novo/", views.cadastrar_genero, name="cadastrar_genero"),
    path("generos/<int:id>/editar/", views.editar_genero, name="editar_genero"),
    path("generos/<int:id>/excluir/", views.excluir_genero, name="excluir_genero"),
    path("plataformas/", views.lista_plataformas, name="lista_plataformas"),
    path("plataformas/novo/", views.cadastrar_plataforma, name="cadastrar_plataforma"),
    path("plataformas/<int:id>/editar/", views.editar_plataforma, name="editar_plataforma"),
    path("plataformas/<int:id>/excluir/", views.excluir_plataforma, name="excluir_plataforma"),
    path("jogo/<int:id>/status/", views.alterar_status_rapido, name="alterar_status_rapido"),
    path("jogo/<int:id>/lista-desejo/", views.adicionar_lista_desejo, name="adicionar_lista_desejo"),
    path("jogo/<int:id>/lista-desejo/remover/", views.remover_lista_desejo, name="remover_lista_desejo"),
    path("jogo/<int:id>/conquista/", views.adicionar_conquista, name="adicionar_conquista"),
    path("jogo/<int:id>/sessao/", views.registrar_sessao, name="registrar_sessao"),
    path("lista-desejos/", views.lista_desejos, name="lista_desejos"),
    path("lista-desejos/<int:item_id>/", views.editar_item_desejo, name="editar_item_desejo"),
    path("conquistas/", views.conquistas_view, name="conquistas"),
    path("estatisticas/", views.estatisticas_view, name="estatisticas"),
    path("configuracoes/", views.configuracoes, name="configuracoes"),
    path("notificacoes/", views.notificacoes_view, name="notificacoes"),
    # Compatibilidade v1
    path("lista/", views.lista_jogos, name="lista_jogos"),
]
