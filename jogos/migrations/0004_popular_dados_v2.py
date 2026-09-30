from django.db import migrations
from django.utils.text import slugify


def popular_dados(apps, schema_editor):
    Genero = apps.get_model("jogos", "Genero")
    Plataforma = apps.get_model("jogos", "Plataforma")
    Jogo = apps.get_model("jogos", "Jogo")

    padroes = [
        "PC",
        "PlayStation 5",
        "PlayStation 4",
        "Xbox Series X|S",
        "Xbox One",
        "Nintendo Switch",
        "Steam Deck",
        "Mobile",
    ]
    for nome in padroes:
        slug = slugify(nome) or "outra"
        Plataforma.objects.get_or_create(slug=slug, defaults={"nome": nome})

    for genero in Genero.objects.all():
        if not genero.slug:
            base = slugify(genero.nome) or f"genero-{genero.pk}"
            genero.slug = base
            genero.save(update_fields=["slug"])

    for jogo in Jogo.objects.all():
        if not jogo.slug:
            base = slugify(jogo.nome) or f"jogo-{jogo.pk}"
            jogo.slug = base
        if jogo.plataforma:
            nome = jogo.plataforma.strip()
            slug = slugify(nome) or "outra"
            plat, _ = Plataforma.objects.get_or_create(
                slug=slug, defaults={"nome": nome}
            )
            jogo.plataforma_ref_id = plat.id
        jogo.save(update_fields=["slug", "plataforma_ref_id"])


class Migration(migrations.Migration):
    dependencies = [
        ("jogos", "0003_plataforma_alter_genero_options_alter_jogo_options_and_more"),
    ]

    operations = [
        migrations.RunPython(popular_dados, migrations.RunPython.noop),
    ]
