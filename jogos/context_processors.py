def notificacoes_nao_lidas(request):
    if not request.user.is_authenticated:
        return {"notificacoes_nao_lidas": 0}
    return {
        "notificacoes_nao_lidas": request.user.notificacoes.filter(
            lida=False
        ).count()
    }
