from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count

from .models import Jogo, Genero
from .forms import JogoForm



def lista_jogos(request):

    jogos = Jogo.objects.all()


    # Pesquisa
    busca = request.GET.get('buscar')


    if busca:

        jogos = jogos.filter(
            nome__icontains=busca
        )


    total_jogos = jogos.count()


    total_generos = Genero.objects.count()


    jogo_mais_caro = jogos.order_by(
        '-preco'
    ).first()


    total_multiplayer = jogos.filter(
        multiplayer=True
    ).count()



    plataformas = list(
        jogos.values(
            'plataforma'
        ).annotate(
            total=Count('id')
        )
    )


    maior_quantidade = 1


    for plataforma in plataformas:

        if plataforma['total'] > maior_quantidade:

            maior_quantidade = plataforma['total']



    for plataforma in plataformas:

        plataforma['porcentagem'] = (
            plataforma['total'] / maior_quantidade
        ) * 100



    return render(
        request,
        'jogos/lista.html',
        {

            'jogos': jogos,

            'busca': busca,

            'total_jogos': total_jogos,

            'total_generos': total_generos,

            'jogo_mais_caro': jogo_mais_caro,

            'total_multiplayer': total_multiplayer,

            'plataformas': plataformas,

        }
    )




def cadastrar_jogo(request):

    if request.method == 'POST':

        form = JogoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Jogo cadastrado com sucesso!'
            )

            return redirect('lista_jogos')


    else:

        form = JogoForm()



    return render(
        request,
        'jogos/form.html',
        {
            'form': form
        }
    )





def editar_jogo(request, id):

    jogo = get_object_or_404(
        Jogo,
        id=id
    )


    if request.method == 'POST':

        form = JogoForm(
            request.POST,
            request.FILES,
            instance=jogo
        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                'Jogo atualizado com sucesso!'
            )


            return redirect(
                'lista_jogos'
            )


    else:

        form = JogoForm(
            instance=jogo
        )



    return render(
        request,
        'jogos/form.html',
        {
            'form':form
        }
    )





def excluir_jogo(request, id):

    jogo = get_object_or_404(
        Jogo,
        id=id
    )


    if request.method == 'POST':

        nome = jogo.nome

        jogo.delete()


        messages.success(
            request,
            f'Jogo "{nome}" excluído!'
        )


        return redirect(
            'lista_jogos'
        )


    return render(
        request,
        'jogos/excluir.html',
        {
            'jogo':jogo
        }
    )





def detalhe_jogo(request,id):

    jogo = get_object_or_404(
        Jogo,
        id=id
    )


    return render(
        request,
        'jogos/detalhe.html',
        {
            'jogo':jogo
        }
    )