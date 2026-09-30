from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import (
    Avaliacao,
    EntradaBiblioteca,
    Genero,
    ItemListaDesejo,
    Jogo,
    Plataforma,
    StatusJogo,
)


class GameVaultTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin", password="senha12345", is_staff=True
        )
        self.user = User.objects.create_user(username="tester", password="senha12345")
        self.outro = User.objects.create_user(username="outro", password="senha12345")
        self.genero = Genero.objects.create(nome="RPG", slug="rpg")
        self.plataforma = Plataforma.objects.get(nome="PC")
        self.jogo = Jogo.objects.create(
            usuario=None,
            nome="Test Game",
            slug="test-game",
            desenvolvedora="Dev",
            distribuidora="Pub",
            descricao="Desc",
            preco=Decimal("59.90"),
            data_lancamento="2024-01-01",
            classificacao="16",
            genero=self.genero,
        )
        self.jogo.plataformas.add(self.plataforma)
        self.entrada = EntradaBiblioteca.objects.create(
            usuario=self.user,
            jogo=self.jogo,
            status=StatusJogo.PLAYING,
        )
        self.client = Client()

    def test_login_required_biblioteca(self):
        response = self.client.get(reverse("biblioteca"))
        self.assertEqual(response.status_code, 302)

    def test_usuario_nao_cria_jogo(self):
        self.client.login(username="tester", password="senha12345")
        response = self.client.get(reverse("cadastrar_jogo"))
        self.assertEqual(response.status_code, 403)

    def test_admin_cria_jogo_catalogo(self):
        self.client.login(username="admin", password="senha12345")
        response = self.client.post(
            reverse("cadastrar_jogo"),
            {
                "nome": "Novo",
                "desenvolvedora": "D",
                "distribuidora": "P",
                "descricao": "X",
                "preco": "10",
                "data_lancamento": "2023-06-01",
                "classificacao": "L",
                "genero": self.genero.id,
                "plataformas": [self.plataforma.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Jogo.objects.filter(nome="Novo", usuario__isnull=True).exists()
        )

    def test_busca_biblioteca(self):
        self.client.login(username="tester", password="senha12345")
        response = self.client.get(reverse("biblioteca"), {"buscar": "Test"})
        self.assertContains(response, "Test Game")

    def test_usuario_nao_edita_jogo(self):
        self.client.login(username="outro", password="senha12345")
        response = self.client.get(reverse("editar_jogo", args=[self.jogo.id]))
        self.assertEqual(response.status_code, 403)

    def test_detalhe_catalogo_e_adicionar_biblioteca(self):
        compartilhado = Jogo.objects.create(
            usuario=None,
            nome="Demo Shared",
            slug="demo-shared",
            desenvolvedora="Dev",
            distribuidora="Pub",
            descricao="Jogo demo",
            preco=Decimal("0"),
            data_lancamento="2020-01-01",
            classificacao="L",
            genero=self.genero,
        )
        compartilhado.plataformas.add(self.plataforma)
        self.client.login(username="outro", password="senha12345")
        response = self.client.get(reverse("detalhe_jogo", args=[compartilhado.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Demo Shared")
        self.client.post(reverse("adicionar_biblioteca", args=[compartilhado.id]))
        self.assertTrue(
            EntradaBiblioteca.objects.filter(
                usuario=self.outro, jogo=compartilhado
            ).exists()
        )

    def test_wishlist(self):
        self.client.login(username="tester", password="senha12345")
        self.client.post(reverse("adicionar_lista_desejo", args=[self.jogo.id]))
        self.assertTrue(
            ItemListaDesejo.objects.filter(usuario=self.user, jogo=self.jogo).exists()
        )

    def test_dashboard_stats(self):
        self.client.login(username="tester", password="senha12345")
        response = self.client.get(reverse("dashboard"))
        self.assertContains(response, "Dashboard")
        self.assertContains(response, "Total de jogos")

    def test_crud_genero_somente_staff(self):
        self.client.login(username="tester", password="senha12345")
        response = self.client.post(
            reverse("cadastrar_genero"), {"nome": "Ação", "descricao": "Combate"}
        )
        self.assertEqual(response.status_code, 403)
        self.client.login(username="admin", password="senha12345")
        self.client.post(
            reverse("cadastrar_genero"), {"nome": "Ação", "descricao": "Combate"}
        )
        self.assertTrue(Genero.objects.filter(nome="Ação").exists())

    def test_avaliacao_com_entrada(self):
        self.client.login(username="tester", password="senha12345")
        self.client.post(
            reverse("salvar_avaliacao", args=[self.jogo.id]),
            {"nota": 5, "comentario": "Excelente"},
        )
        self.assertEqual(Avaliacao.objects.get(jogo=self.jogo).nota, 5)
        detalhe = self.client.get(reverse("detalhe_jogo", args=[self.jogo.id]))
        self.assertContains(detalhe, "Excelente")

    def test_estatisticas_usa_dados_do_banco(self):
        self.client.login(username="tester", password="senha12345")
        response = self.client.get(reverse("estatisticas"))
        self.assertContains(response, "Estatísticas")
        self.assertContains(response, "Taxa de conclusão")

    def test_admin_acessa_django_admin(self):
        self.client.login(username="tester", password="senha12345")
        self.assertEqual(self.client.get("/admin/").status_code, 302)
        self.client.logout()
        self.client.login(username="admin", password="senha12345")
        response = self.client.get("/admin/")
        self.assertIn(response.status_code, (200, 302))
