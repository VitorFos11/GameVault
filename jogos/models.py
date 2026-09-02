from django.db import models


class Genero(models.Model):

    nome = models.CharField(max_length=100)

    descricao = models.TextField(
        max_length=300,
        blank=True
    )


    def __str__(self):
        return self.nome



class Jogo(models.Model):

    nome = models.CharField(max_length=100)

    desenvolvedora = models.CharField(max_length=100)

    distribuidora = models.CharField(max_length=100)

    plataforma = models.CharField(max_length=100)

    descricao = models.TextField(
        max_length=500
    )

    preco = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    data_lancamento = models.DateField()

    classificacao = models.CharField(
        max_length=50
    )

    multiplayer = models.BooleanField(
        default=False
    )

    genero = models.ForeignKey(
        Genero,
        on_delete=models.CASCADE,
        related_name="jogos"
    )

 # NOVO CAMPO
    capa = models.ImageField(
        upload_to="capas/",
        blank=True,
        null=True
    )


    def __str__(self):
        return self.nome