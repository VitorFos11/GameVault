"""
Gera capturas em docs/assets/telas/ para o README (UI v2).
Requer: pip install playwright && python -m playwright install chromium
Servidor: python manage.py runserver 8765 (em outro terminal)
"""

from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "docs" / "assets" / "telas"
BASE_URL = "http://127.0.0.1:8765"


def _ensure_demo_user():
    import os
    import sys

    import django

    sys.path.insert(0, str(BASE))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gamevault.settings")
    django.setup()
    from django.contrib.auth import get_user_model

    User = get_user_model()
    if not User.objects.filter(username="demo").exists():
        User.objects.create_user(username="demo", password="demo123456", email="demo@gamevault.local")


def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit("Instale playwright: pip install playwright") from exc

    OUT.mkdir(parents=True, exist_ok=True)

    public_pages = [
        ("01-landing.png", "/"),
        ("02-login.png", "/conta/login/"),
    ]
    auth_pages = [
        ("04-dashboard.png", "/dashboard/"),
        ("05-biblioteca.png", "/biblioteca/"),
        ("07-formulario.png", "/novo/"),
        ("08-wishlist.png", "/lista-desejos/"),
        ("10-estatisticas.png", "/estatisticas/"),
        ("11-catalogo-generos.png", "/generos/"),
        ("09-perfil.png", "/conta/perfil/"),
        ("12-configuracoes.png", "/configuracoes/"),
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        for name, path in public_pages:
            page.goto(f"{BASE_URL}{path}")
            page.wait_for_timeout(700)
            page.screenshot(path=str(OUT / name), full_page=True)
            print("OK", name)

        page.goto(f"{BASE_URL}/conta/login/")
        page.fill('input[name="username"]', "demo")
        page.fill('input[name="password"]', "demo123456")
        page.get_by_role("button", name="Entrar").click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(500)

        page.goto(f"{BASE_URL}/biblioteca/")
        page.wait_for_timeout(600)
        link = page.locator("a[href*='/jogo/']").first
        if link.count():
            href = link.get_attribute("href") or ""
            url = href if href.startswith("http") else f"{BASE_URL}{href}"
            page.goto(url)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)
            page.locator(".gv-topbar").get_by_role("button", name="Sair").wait_for(
                state="visible", timeout=8000
            )
            page.screenshot(path=str(OUT / "06-detalhe.png"), full_page=False)
            print("OK", "06-detalhe.png")
        else:
            print("SKIP 06-detalhe.png (sem jogos na biblioteca demo)")

        def shot_authenticated(name: str, path: str) -> None:
            page.goto(f"{BASE_URL}{path}")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)
            page.locator(".gv-sidebar-footer").get_by_role(
                "button", name="Sair e trocar usuário"
            ).wait_for(state="visible", timeout=8000)
            page.locator(".gv-topbar").get_by_role("button", name="Sair").wait_for(
                state="visible", timeout=8000
            )
            # Viewport (não full_page) mantém sidebar + botão Sair legíveis no README.
            page.screenshot(path=str(OUT / name), full_page=False)
            print("OK", name)

        for name, path in auth_pages:
            shot_authenticated(name, path)

        browser.close()


if __name__ == "__main__":
    _ensure_demo_user()
    main()
