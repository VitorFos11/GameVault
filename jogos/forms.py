from django import forms

from .models import (
    Avaliacao,
    Conquista,
    Genero,
    ItemListaDesejo,
    Jogo,
    Plataforma,
    SessaoJogo,
)


def _estilizar_campos(form):
    for field in form.fields.values():
        if isinstance(field.widget, forms.CheckboxInput):
            continue
        if isinstance(field.widget, forms.CheckboxSelectMultiple):
            field.widget.attrs["class"] = "gv-checklist"
            continue
        field.widget.attrs.setdefault("class", "gv-input")


class JogoForm(forms.ModelForm):
    class Meta:
        model = Jogo
        fields = [
            "nome",
            "desenvolvedora",
            "distribuidora",
            "plataformas",
            "descricao",
            "preco",
            "preco_compra",
            "data_lancamento",
            "classificacao",
            "multiplayer",
            "genero",
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
            "plataformas": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["plataformas"].label = "Plataformas"
        self.fields["genero"].label = "Gênero"
        self.fields["plataformas"].help_text = "Marque uma ou mais plataformas."
        _estilizar_campos(self)

    def save(self, commit=True):
        jogo = super().save(commit=commit)
        if commit and jogo.genero_id:
            jogo.generos.add(jogo.genero)
        return jogo


class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ["nome", "descricao"]
        widgets = {"descricao": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _estilizar_campos(self)


class PlataformaForm(forms.ModelForm):
    class Meta:
        model = Plataforma
        fields = ["nome", "fabricante", "descricao"]
        widgets = {"descricao": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _estilizar_campos(self)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nota"].help_text = "De 1 a 5."
        _estilizar_campos(self)


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
