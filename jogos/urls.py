from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.lista_jogos,
        name='lista_jogos'
    ),

    path(
        'novo/',
        views.cadastrar_jogo,
        name='cadastrar_jogo'
    ),

    path(
        'jogo/<int:id>/',
        views.detalhe_jogo,
        name='detalhe_jogo'
    ),

    path(
        'editar/<int:id>/',
        views.editar_jogo,
        name='editar_jogo'
    ),

    path(
        'excluir/<int:id>/',
        views.excluir_jogo,
        name='excluir_jogo'
    ),

]