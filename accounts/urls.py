from django.urls import path

from .views import GameVaultLoginView, GameVaultLogoutView, perfil, registro

app_name = "accounts"

urlpatterns = [
    path("login/", GameVaultLoginView.as_view(), name="login"),
    path("logout/", GameVaultLogoutView.as_view(), name="logout"),
    path("registro/", registro, name="registro"),
    path("perfil/", perfil, name="perfil"),
]
