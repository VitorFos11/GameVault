"""
Gera capturas em docs/assets/telas/ para o README.
Requer: pip install playwright && python -m playwright install chromium
Servidor: python manage.py runserver 8765 (em outro terminal)
"""

from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "docs" / "assets" / "telas"
BASE_URL = "http://127.0.0.1:8765"

PAGES = [
    ("01-landing.png", "/"),
    ("02-login.png", "/conta/login/"),
    ("03-registro.png", "/conta/registro/"),
    ("04-dashboard.png", "/dashboard/"),
    ("05-biblioteca.png", "/biblioteca/"),
    ("07-formulario.png", "/novo/"),
    ("08-wishlist.png", "/lista-desejos/"),
    ("09-perfil.png", "/conta/perfil/"),
]


def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit("Instale playwright: pip install playwright") from exc

    OUT.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        page.goto(f"{BASE_URL}/conta/login/")
        page.fill('input[name="username"]', "demo")
        page.fill('input[name="password"]', "demo123456")
        page.click('button[type="submit"]')
        page.wait_for_timeout(800)

        for name, path in PAGES:
            page.goto(f"{BASE_URL}{path}")
            page.wait_for_timeout(600)
            page.screenshot(path=str(OUT / name), full_page=True)
            print("OK", name)

        browser.close()


if __name__ == "__main__":
    main()
