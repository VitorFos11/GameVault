from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Avaliacao, Genero, ItemListaDesejo, Jogo, Plataforma, StatusJogo


class GameVaultTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="senha12345")
        self.outro = User.objects.create_user(username="outro", password="senha12345")
        self.genero = Genero.objects.create(nome="RPG", slug="rpg")
        self.plataforma = Plataforma.objects.get(nome="PC")
        self.jogo = Jogo.objects.create(
            usuario=self.user,
            nome="Test Game",
            slug="test-game",
            desenvolvedora="Dev",
            distribuidora="Pub",
            descricao="Desc",
            preco=Decimal("59.90"),
            data_lancamento="2024-01-01",
            classificacao="16",
            genero=self.genero,
            status=StatusJogo.PLAYING,
        )
        self.jogo.plataformas.add(self.plataforma)
        self.client = Client()

    def test_login_required_biblioteca(self):
        response = self.client.get(reverse("biblioteca"))
        self.assertEqual(response.status_code, 302)

    def test_criar_jogo_autenticado(self):
        self.client.login(username="tester", password="senha12345")
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
                "status": StatusJogo.BACKLOG,
                "horas_jogadas": "0",
                "percentual_conclusao": "0",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Jogo.objects.filter(nome="Novo", usuario=self.user).exists())

    def test_busca_biblioteca(self):
        self.client.login(username="tester", password="senha12345")
        response = self.client.get(reverse("biblioteca"), {"buscar": "Test"})
        self.assertContains(response, "Test Game")

    def test_autorizacao_outro_usuario(self):
        self.client.login(username="outro", password="senha12345")
        response = self.client.get(reverse("editar_jogo", args=[self.jogo.id]))
        self.assertEqual(response.status_code, 403)

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
        self.assertContains(response, "Total de gêneros")
        self.assertContains(response, "RPG")

    def test_crud_genero_e_plataforma(self):
        self.client.login(username="tester", password="senha12345")
        self.client.post(reverse("cadastrar_genero"), {"nome": "Ação", "descricao": "Combate"})
        self.assertTrue(Genero.objects.filter(nome="Ação").exists())
        genero = Genero.objects.get(nome="Ação")
        self.client.post(
            reverse("editar_genero", args=[genero.id]),
            {"nome": "Ação", "descricao": "Ação e aventura"},
        )
        genero.refresh_from_db()
        self.assertEqual(genero.descricao, "Ação e aventura")

        self.client.post(
            reverse("cadastrar_plataforma"),
            {"nome": "Neo Geo", "fabricante": "SNK", "descricao": "Arcade"},
        )
        plataforma = Plataforma.objects.get(nome="Neo Geo")
        response = self.client.post(
            reverse("cadastrar_jogo"),
            {
                "nome": "GTA V",
                "desenvolvedora": "Rockstar",
                "distribuidora": "Rockstar",
                "descricao": "Mundo aberto",
                "preco": "99.90",
                "data_lancamento": "2013-09-17",
                "classificacao": "18",
                "genero": self.genero.id,
                "plataformas": [plataforma.id],
                "status": StatusJogo.BACKLOG,
                "horas_jogadas": "0",
                "percentual_conclusao": "0",
            },
        )
        jogo = Jogo.objects.get(nome="GTA V")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(jogo.genero, self.genero)
        self.assertIn(plataforma, jogo.plataformas.all())

        self.client.post(
            reverse("salvar_avaliacao", args=[jogo.id]),
            {"nota": 5, "comentario": "Excelente"},
        )
        self.assertEqual(Avaliacao.objects.get(jogo=jogo).nota, 5)
        detalhe = self.client.get(reverse("detalhe_jogo", args=[jogo.id]))
        self.assertContains(detalhe, "Excelente")
        self.assertContains(detalhe, self.genero.nome)
        self.assertContains(detalhe, plataforma.nome)

        painel = self.client.get(reverse("dashboard"))
        self.assertContains(painel, "Total de avaliações")
        self.assertContains(painel, "99,90")

        self.client.post(reverse("excluir_genero", args=[self.genero.id]))
        self.assertTrue(Genero.objects.filter(pk=self.genero.id).exists())
        self.client.post(reverse("excluir_plataforma", args=[plataforma.id]))
        self.assertTrue(Plataforma.objects.filter(pk=plataforma.id).exists())

    def test_estatisticas_usa_dados_do_banco(self):
        self.client.login(username="tester", password="senha12345")
        response = self.client.get(reverse("estatisticas"))
        self.assertContains(response, "Estatísticas")
        self.assertContains(response, "Taxa de conclusão")
