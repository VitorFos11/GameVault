from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class LogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="senha12345")
        self.client = Client()

    def test_logout_redireciona_para_login(self):
        self.client.login(username="tester", password="senha12345")
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
