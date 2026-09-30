from decimal import Decimal

from django.conf import settings
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


def migrar_biblioteca_e_catalogo(apps, schema_editor):
    Jogo = apps.get_model("jogos", "Jogo")
    EntradaBiblioteca = apps.get_model("jogos", "EntradaBiblioteca")
    Conquista = apps.get_model("jogos", "Conquista")
    User = apps.get_model("auth", "User")

    staff = User.objects.filter(is_staff=True).order_by("id").first()

    for jogo in Jogo.objects.all().iterator():
        owner_id = jogo.usuario_id
        if owner_id:
            EntradaBiblioteca.objects.get_or_create(
                usuario_id=owner_id,
                jogo_id=jogo.id,
                defaults={
                    "status": jogo.status,
                    "horas_jogadas": jogo.horas_jogadas or Decimal("0"),
                    "percentual_conclusao": jogo.percentual_conclusao or 0,
                    "avaliacao_pessoal": jogo.avaliacao_pessoal,
                    "ultimo_jogado": jogo.ultimo_jogado,
                },
            )
        Jogo.objects.filter(pk=jogo.pk).update(usuario=None)

        for conquista in Conquista.objects.filter(jogo_id=jogo.id, usuario__isnull=True):
            uid = owner_id or (staff.id if staff else None)
            if uid:
                conquista.usuario_id = uid
                conquista.save(update_fields=["usuario_id"])


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("jogos", "0009_remove_jogo_fonte_dados_remove_jogo_fonte_url_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="EntradaBiblioteca",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("wishlist", "Lista de desejos"),
                            ("backlog", "Backlog"),
                            ("playing", "Jogando"),
                            ("paused", "Pausado"),
                            ("completed", "Concluído"),
                            ("mastered", "Masterizado"),
                            ("dropped", "Abandonado"),
                        ],
                        default="backlog",
                        max_length=20,
                    ),
                ),
                (
                    "horas_jogadas",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=8,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "percentual_conclusao",
                    models.PositiveSmallIntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
                (
                    "avaliacao_pessoal",
                    models.DecimalField(
                        blank=True,
                        decimal_places=1,
                        max_digits=3,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(5),
                        ],
                    ),
                ),
                ("ultimo_jogado", models.DateTimeField(blank=True, null=True)),
                ("adicionado_em", models.DateTimeField(auto_now_add=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
                (
                    "jogo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entradas_biblioteca",
                        to="jogos.jogo",
                    ),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entradas_biblioteca",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Entrada na biblioteca",
                "verbose_name_plural": "Entradas na biblioteca",
                "ordering": ["-adicionado_em"],
                "unique_together": {("usuario", "jogo")},
            },
        ),
        migrations.AddField(
            model_name="conquista",
            name="usuario",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="conquistas",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(migrar_biblioteca_e_catalogo, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="conquista",
            name="usuario",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="conquistas",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
