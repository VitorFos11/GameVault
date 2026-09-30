from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from gamevault.admin_site import GameVaultAdminSite

# Substitui o admin padrão pelo admin customizado
admin.site.__class__ = GameVaultAdminSite

urlpatterns = [
    path("admin/", admin.site.urls),
    path("conta/", include("accounts.urls")),
    path("", include("jogos.urls")),
]

handler404 = "jogos.error_views.erro_404"
handler403 = "jogos.error_views.erro_403"
handler500 = "jogos.error_views.erro_500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
