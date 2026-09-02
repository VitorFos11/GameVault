from django import forms
from .models import Jogo


class JogoForm(forms.ModelForm):

    class Meta:
        model = Jogo

        fields = [
            'nome',
            'desenvolvedora',
            'distribuidora',
            'plataforma',
            'descricao',
            'preco',
            'data_lancamento',
            'classificacao',
            'multiplayer',
            'genero',
            'capa'
        ]

        widgets = {

            'data_lancamento': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'descricao': forms.Textarea(
                attrs={
                    'rows': 4
                }
            )
        }