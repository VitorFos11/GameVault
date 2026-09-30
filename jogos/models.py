from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class Genero(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    descricao = models.TextField(max_length=300, blank=True, verbose_name="Descrição")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Gênero"
        verbose_name_plural = "Gêneros"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.nome) or "genero"
            slug = base
            n = 1
            while Genero.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Plataforma(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    fabricante = models.CharField(max_length=120, blank=True, verbose_name="Fabricante")
    descricao = models.TextField(max_length=300, blank=True, verbose_name="Descrição")
    icone = models.CharField(max_length=80, blank=True, help_text="Classe ou rótulo curto do ícone")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Plataforma"
        verbose_name_plural = "Plataformas"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.nome) or "plataforma"
            slug = base
            n = 1
            while Plataforma.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class StatusJogo(models.TextChoices):
    WISHLIST = "wishlist", "Lista de desejos"
    BACKLOG = "backlog", "Backlog"
    PLAYING = "playing", "Jogando"
    PAUSED = "paused", "Pausado"
    COMPLETED = "completed", "Concluído"
    MASTERED = "mastered", "Masterizado"
    DROPPED = "dropped", "Abandonado"


class Jogo(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jogos",
        null=True,
        blank=True,
    )
    nome = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, blank=True)
    desenvolvedora = models.CharField(max_length=150)
    distribuidora = models.CharField(max_length=150)
    plataformas = models.ManyToManyField(
        Plataforma,
        blank=True,
        related_name="jogos",
        verbose_name="Plataformas",
    )
    descricao = models.TextField(max_length=2000)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    preco_compra = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    data_lancamento = models.DateField()
    classificacao = models.CharField(max_length=50)
    multiplayer = models.BooleanField(default=False)
    genero = models.ForeignKey(
        Genero,
        on_delete=models.PROTECT,
        related_name="jogos",
        verbose_name="Gênero",
    )
    generos = models.ManyToManyField(
        Genero,
        blank=True,
        related_name="jogos_extra",
    )
    capa = models.ImageField(upload_to="capas/", blank=True, null=True)
    banner = models.ImageField(upload_to="banners/", blank=True, null=True)
    website = models.URLField(blank=True)
    tags = models.CharField(max_length=500, blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusJogo.choices,
        default=StatusJogo.BACKLOG,
    )
    horas_jogadas = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    percentual_conclusao = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    avaliacao_pessoal = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    ultimo_jogado = models.DateTimeField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ["-criado_em", "-id"]
        verbose_name = "Jogo"
        verbose_name_plural = "Jogos"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.nome) or "jogo"
            slug = base
            n = 1
            while (
                Jogo.objects.filter(slug=slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def nome_plataforma(self):
        # .all() aproveita o prefetch_related das listagens; values_list abriria nova query.
        nomes = [plataforma.nome for plataforma in self.plataformas.all()]
        return ", ".join(nomes) or "Não informada"

    def __str__(self):
        return self.nome


class EntradaBiblioteca(models.Model):
    """Vínculo usuário ↔ jogo do catálogo (progresso pessoal)."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="entradas_biblioteca",
    )
    jogo = models.ForeignKey(
        Jogo,
        on_delete=models.CASCADE,
        related_name="entradas_biblioteca",
    )
    status = models.CharField(
        max_length=20,
        choices=StatusJogo.choices,
        default=StatusJogo.BACKLOG,
    )
    horas_jogadas = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    percentual_conclusao = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    avaliacao_pessoal = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    ultimo_jogado = models.DateTimeField(null=True, blank=True)
    adicionado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [["usuario", "jogo"]]
        ordering = ["-adicionado_em"]
        verbose_name = "Entrada na biblioteca"
        verbose_name_plural = "Entradas na biblioteca"

    def __str__(self):
        return f"{self.usuario} — {self.jogo.nome}"


class PrioridadeDesejo(models.TextChoices):
    LOW = "low", "Baixa"
    MEDIUM = "medium", "Média"
    HIGH = "high", "Alta"


class ItemListaDesejo(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lista_desejos",
    )
    jogo = models.ForeignKey(
        Jogo,
        on_delete=models.CASCADE,
        related_name="itens_lista_desejo",
    )
    prioridade = models.CharField(
        max_length=10,
        choices=PrioridadeDesejo.choices,
        default=PrioridadeDesejo.MEDIUM,
    )
    preco_alvo = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    preco_atual = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    notas = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["usuario", "jogo"]]
        ordering = ["-prioridade", "-criado_em"]

    def __str__(self):
        return f"{self.usuario} — {self.jogo.nome}"


class Avaliacao(models.Model):
    jogo = models.ForeignKey(
        Jogo,
        on_delete=models.CASCADE,
        related_name="avaliacoes",
        verbose_name="Jogo",
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="avaliacoes",
    )
    nota = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Nota",
    )
    comentario = models.TextField(blank=True, verbose_name="Comentário")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [["usuario", "jogo"]]
        ordering = ["-atualizado_em"]
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    def __str__(self):
        return f"{self.nota}/5 — {self.jogo.nome}"


class Conquista(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conquistas",
    )
    jogo = models.ForeignKey(
        Jogo,
        on_delete=models.CASCADE,
        related_name="conquistas",
    )
    nome = models.CharField(max_length=150)
    descricao = models.CharField(max_length=400, blank=True)
    icone = models.CharField(max_length=80, blank=True, default="trophy")
    concluida = models.BooleanField(default=False)
    concluida_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["concluida", "nome"]

    def __str__(self):
        return self.nome


class SessaoJogo(models.Model):
    jogo = models.ForeignKey(
        Jogo,
        on_delete=models.CASCADE,
        related_name="sessoes",
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessoes_jogo",
    )
    iniciado_em = models.DateTimeField()
    terminado_em = models.DateTimeField(null=True, blank=True)
    duracao_minutos = models.PositiveIntegerField(default=0)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["-iniciado_em"]

    def __str__(self):
        return f"{self.jogo.nome} — {self.iniciado_em.date()}"


class TipoNotificacao(models.TextChoices):
    JOGO_CONCLUIDO = "game_completed", "Jogo concluído"
    LISTA_DESEJO = "wishlist", "Lista de desejos"
    CONQUISTA = "achievement", "Conquista"
    AVALIACAO = "review", "Avaliação"
    GERAL = "general", "Geral"


class Notificacao(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notificacoes",
    )
    tipo = models.CharField(
        max_length=30,
        choices=TipoNotificacao.choices,
        default=TipoNotificacao.GERAL,
    )
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField(blank=True)
    lida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return self.titulo
