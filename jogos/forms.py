from django import forms

from .models import (
    Avaliacao,
    Conquista,
    ItemListaDesejo,
    Jogo,
    SessaoJogo,
)


class JogoForm(forms.ModelForm):
    class Meta:
        model = Jogo
        fields = [
            "nome",
            "desenvolvedora",
            "distribuidora",
            "plataforma_ref",
            "descricao",
            "preco",
            "preco_compra",
            "data_lancamento",
            "classificacao",
            "multiplayer",
            "genero",
            "generos",
            "capa",
            "banner",
            "website",
            "tags",
            "status",
            "avaliacao_pessoal",
            "horas_jogadas",
            "percentual_conclusao",
        ]
        widgets = {
            "data_lancamento": forms.DateInput(attrs={"type": "date"}),
            "descricao": forms.Textarea(attrs={"rows": 5}),
            "tags": forms.TextInput(
                attrs={"placeholder": "Ex.: rpg, open-world, coop"}
            ),
            "generos": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = "gv-input"
            if isinstance(field.widget, forms.CheckboxInput):
                continue
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs["class"] = "gv-checklist"
                continue
            field.widget.attrs.setdefault("class", css)


class ProgressoJogoForm(forms.ModelForm):
    class Meta:
        model = Jogo
        fields = ["horas_jogadas", "percentual_conclusao", "status"]
        widgets = {
            "horas_jogadas": forms.NumberInput(attrs={"step": "0.5", "min": "0"}),
            "percentual_conclusao": forms.NumberInput(
                attrs={"min": "0", "max": "100"}
            ),
        }


class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ["nota", "comentario"]
        widgets = {
            "nota": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "comentario": forms.Textarea(attrs={"rows": 4}),
        }


class ItemListaDesejoForm(forms.ModelForm):
    class Meta:
        model = ItemListaDesejo
        fields = ["prioridade", "preco_alvo", "preco_atual", "notas"]
        widgets = {"notas": forms.Textarea(attrs={"rows": 3})}


class ConquistaForm(forms.ModelForm):
    class Meta:
        model = Conquista
        fields = ["nome", "descricao", "icone", "concluida"]


class SessaoJogoForm(forms.ModelForm):
    class Meta:
        model = SessaoJogo
        fields = ["iniciado_em", "terminado_em", "duracao_minutos", "notas"]
        widgets = {
            "iniciado_em": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "terminado_em": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "notas": forms.Textarea(attrs={"rows": 2}),
        }


class BuscaImportacaoForm(forms.Form):
    q = forms.CharField(
        label="Buscar jogo externo",
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "Nome do jogo na RAWG..."}),
    )
