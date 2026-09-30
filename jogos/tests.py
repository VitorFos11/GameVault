from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Genero, ItemListaDesejo, Jogo, StatusJogo


class GameVaultTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="senha12345")
        self.outro = User.objects.create_user(username="outro", password="senha12345")
        self.genero = Genero.objects.create(nome="RPG", slug="rpg")
        self.jogo = Jogo.objects.create(
            usuario=self.user,
            nome="Test Game",
            slug="test-game",
            desenvolvedora="Dev",
            distribuidora="Pub",
            plataforma="PC",
            descricao="Desc",
            preco=Decimal("59.90"),
            data_lancamento="2024-01-01",
            classificacao="16",
            genero=self.genero,
            status=StatusJogo.PLAYING,
        )
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
        self.assertContains(response, "1")
