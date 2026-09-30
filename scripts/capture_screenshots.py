"""
Gera capturas em docs/assets/telas/ para o README (UI v2).
Requer: pip install playwright && python -m playwright install chromium
Servidor: python manage.py runserver 8765 (em outro terminal)
"""

from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "docs" / "assets" / "telas"
BASE_URL = "http://127.0.0.1:8765"


def _ensure_users_and_library():
    import os
    import sys

    import django

    sys.path.insert(0, str(BASE))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gamevault.settings")
    django.setup()
    from django.contrib.auth import get_user_model

    from jogos.models import EntradaBiblioteca, Jogo, StatusJogo

    User = get_user_model()
    if not User.objects.filter(username="demo").exists():
        User.objects.create_user(
            username="demo", password="demo123456", email="demo@gamevault.local"
        )
    demo = User.objects.get(username="demo")
    staff, created = User.objects.get_or_create(
        username="staff_demo",
        defaults={"email": "staff@gamevault.local", "is_staff": True},
    )
    if created or not staff.is_staff:
        staff.is_staff = True
        staff.set_password("demo123456")
        staff.save()

    for jogo in Jogo.objects.filter(usuario__isnull=True):
        EntradaBiblioteca.objects.get_or_create(
            usuario=demo,
            jogo=jogo,
            defaults={"status": StatusJogo.BACKLOG},
        )


def _logout(page) -> None:
    if page.locator(".gv-topbar").get_by_role("button", name="Sair").count():
        page.locator(".gv-topbar").get_by_role("button", name="Sair").click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(400)


def _login(page, username: str) -> None:
    _logout(page)
    page.goto(f"{BASE_URL}/conta/login/")
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', "demo123456")
    page.get_by_role("button", name="Entrar").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(500)


def _shot(page, filename: str, path: str, *, viewport_only: bool = True) -> None:
    page.goto(f"{BASE_URL}{path}")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(600)
    if path not in ("/", "/conta/login/"):
        page.locator(".gv-topbar").get_by_role("button", name="Sair").wait_for(
            state="visible", timeout=8000
        )
    page.screenshot(
        path=str(OUT / filename),
        full_page=not viewport_only,
    )
    print("OK", filename)


def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit("Instale playwright: pip install playwright") from exc

    OUT.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        _shot(page, "01-landing.png", "/", viewport_only=False)
        _shot(page, "02-login.png", "/conta/login/", viewport_only=False)

        _login(page, "demo")
        _shot(page, "04-dashboard.png", "/dashboard/")
        _shot(page, "13-explorar.png", "/explorar/")
        _shot(page, "05-biblioteca.png", "/biblioteca/")

        page.goto(f"{BASE_URL}/biblioteca/")
        page.wait_for_timeout(500)
        link = page.locator("a[href*='/jogo/']").first
        if link.count():
            href = link.get_attribute("href") or ""
            url = href if href.startswith("http") else f"{BASE_URL}{href}"
            page.goto(url)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)
            page.screenshot(path=str(OUT / "06-detalhe.png"), full_page=False)
            print("OK", "06-detalhe.png")
        else:
            print("SKIP 06-detalhe.png")

        _shot(page, "08-wishlist.png", "/lista-desejos/")
        _shot(page, "10-estatisticas.png", "/estatisticas/")
        _shot(page, "09-perfil.png", "/conta/perfil/")
        _shot(page, "12-configuracoes.png", "/configuracoes/")
        _shot(page, "11-catalogo-generos.png", "/generos/")

        _login(page, "staff_demo")
        _shot(page, "07-formulario.png", "/novo/")

        browser.close()


if __name__ == "__main__":
    _ensure_users_and_library()
    main()
