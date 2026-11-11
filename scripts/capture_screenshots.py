"""
Gera capturas em docs/assets/telas/ para o README (UI v2).

Requer: pip install playwright && python -m playwright install chromium
Servidor: python manage.py runserver 8765 (em outro terminal)

Uso:
    python scripts/capture_screenshots.py              # prepara contas demo + biblioteca vazia
    python scripts/capture_screenshots.py --no-seed    # não escreve nada no banco (só captura)

O script só mexe nas contas descartáveis `demo` e `staff_demo` e, no máximo,
popula a biblioteca do `demo` quando ela está vazia (idempotente).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "docs" / "assets" / "telas"
BASE_URL = "http://127.0.0.1:8765"
DEMO_PASSWORD = "demo123456"
TIMEOUT_MS = 8000

TOPBAR_LOGOUT = ".gv-topbar button:has-text('Sair')"


def _ensure_users_and_library(*, seed_library: bool = True) -> None:
    import os

    import django

    sys.path.insert(0, str(BASE))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gamevault.settings")
    django.setup()
    from django.contrib.auth import get_user_model

    from jogos.models import EntradaBiblioteca, Jogo, StatusJogo

    User = get_user_model()

    def _upsert(username: str, email: str, *, is_staff: bool):
        # Sempre redefine senha/flags: garante login mesmo com usuário pré-existente.
        user, _ = User.objects.get_or_create(username=username, defaults={"email": email})
        user.is_staff = is_staff
        user.is_active = True
        user.set_password(DEMO_PASSWORD)
        user.save()
        return user

    demo = _upsert("demo", "demo@gamevault.local", is_staff=False)
    _upsert("staff_demo", "staff@gamevault.local", is_staff=True)

    if not seed_library:
        return
    # Só popula se a biblioteca estiver vazia: evita churn no db.sqlite3 a cada execução.
    if EntradaBiblioteca.objects.filter(usuario=demo).exists():
        return
    catalogo = Jogo.objects.filter(usuario__isnull=True)
    if not catalogo.exists():
        raise SystemExit(
            "Catálogo global vazio (Jogo com usuario nulo): nada para mostrar nas capturas."
        )
    EntradaBiblioteca.objects.bulk_create(
        EntradaBiblioteca(usuario=demo, jogo=j, status=StatusJogo.BACKLOG) for j in catalogo
    )


def _is_logged_in(page) -> bool:
    return page.locator(TOPBAR_LOGOUT).count() > 0


def _logout(page) -> None:
    if _is_logged_in(page):
        page.locator(TOPBAR_LOGOUT).first.click()
        page.wait_for_load_state("networkidle")
    # Confirma o estado: após sair, o botão Sair da topbar não pode existir.
    page.goto(f"{BASE_URL}/conta/login/")
    page.wait_for_selector('input[name="username"]', timeout=TIMEOUT_MS)


def _login(page, username: str) -> None:
    _logout(page)
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', DEMO_PASSWORD)
    page.get_by_role("button", name="Entrar").click()
    page.wait_for_load_state("networkidle")
    try:
        page.locator(TOPBAR_LOGOUT).first.wait_for(state="visible", timeout=TIMEOUT_MS)
    except Exception as exc:
        raise SystemExit(f"Login de '{username}' falhou (verifique usuário/senha).") from exc


def _capture(page, filename: str, *, public: bool, full_page: bool) -> None:
    """Espera a página estabilizar (e o chrome autenticado, se privada) e salva o PNG."""
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(600)
    if not public:
        page.locator(TOPBAR_LOGOUT).first.wait_for(state="visible", timeout=TIMEOUT_MS)
    page.screenshot(path=str(OUT / filename), full_page=full_page)
    print("OK", filename)


def _shot(page, filename: str, path: str, *, public: bool = False, full_page: bool = False) -> None:
    page.goto(f"{BASE_URL}{path}")
    _capture(page, filename, public=public, full_page=full_page)


def _shot_first_game_detail(page, filename: str) -> None:
    page.goto(f"{BASE_URL}/biblioteca/")
    page.wait_for_load_state("networkidle")
    # Restringe ao conteúdo principal: ignora links de sidebar/topbar.
    link = page.locator("#main-content a[href*='/jogo/']").first
    if not link.count():
        raise SystemExit(
            "Nenhum jogo na biblioteca do demo: rode sem --no-seed ou popule o catálogo."
        )
    link.click()
    _capture(page, filename, public=False, full_page=False)


def main() -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit("Instale playwright: pip install playwright") from exc

    OUT.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 1440, "height": 900})

            _shot(page, "01-landing.png", "/", public=True, full_page=True)
            _shot(page, "02-login.png", "/conta/login/", public=True, full_page=True)

            _login(page, "demo")
            _shot(page, "04-dashboard.png", "/dashboard/")
            _shot(page, "13-explorar.png", "/explorar/")
            _shot(page, "05-biblioteca.png", "/biblioteca/")
            _shot_first_game_detail(page, "06-detalhe.png")
            _shot(page, "08-wishlist.png", "/lista-desejos/")
            _shot(page, "10-estatisticas.png", "/estatisticas/")
            _shot(page, "09-perfil.png", "/conta/perfil/")
            _shot(page, "12-configuracoes.png", "/configuracoes/")
            _shot(page, "11-catalogo-generos.png", "/generos/")

            _login(page, "staff_demo")
            _shot(page, "07-formulario.png", "/novo/")
            if "/novo" not in page.url:
                raise SystemExit(f"staff_demo não acessou /novo/ (URL atual: {page.url}).")
        finally:
            browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument(
        "--no-seed",
        action="store_true",
        help="não grava no banco (contas e biblioteca); só captura",
    )
    args = parser.parse_args()
    if not args.no_seed:
        _ensure_users_and_library()
    main()
