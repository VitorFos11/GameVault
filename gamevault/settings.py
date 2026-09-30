"""
Django settings for GameVault.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-dev-only-change-in-production",
)

DEBUG = os.environ.get("DEBUG", "True").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if h.strip()
]

INSTALLED_APPS = [
    "jazzmin",                          # deve vir ANTES do django.contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "jogos",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "gamevault.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "jogos.context_processors.notificacoes_nao_lidas",
            ],
        },
    },
]

WSGI_APPLICATION = "gamevault.wsgi.application"

DATABASE_URL = os.environ.get("DATABASE_URL", "")

if DATABASE_URL.startswith("postgres"):
    import urllib.parse

    url = urllib.parse.urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": url.path[1:],
            "USER": url.username,
            "PASSWORD": url.password,
            "HOST": url.hostname,
            "PORT": url.port or 5432,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "landing"

GAMES_PER_PAGE = int(os.environ.get("GAMES_PER_PAGE", "12"))

# ──────────────────────────────────────────────
# JAZZMIN — Admin GameVault
# ──────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    # ── Identidade ─────────────────────────────
    "site_title": "GameVault Admin",
    "site_header": "GameVault",
    "site_brand": "GameVault",
    "site_logo": "img/logo-icon.svg",
    "site_logo_classes": "img-circle elevation-0",
    "site_icon": "img/logo-icon.svg",
    "welcome_sign": "GameVault — Painel Administrativo",
    "copyright": "GameVault © 2026",

    # ── Busca rápida ────────────────────────────
    "search_model": ["jogos.Jogo", "auth.User"],

    # ── Avatar no topo ──────────────────────────
    "user_avatar": None,

    # ── Topmenu ─────────────────────────────────
    "topmenu_links": [
        {"name": "Ver site", "url": "/", "new_window": False, "icon": "fas fa-home"},
        {"name": "Biblioteca", "url": "/biblioteca/", "new_window": False, "icon": "fas fa-gamepad"},
        {"model": "auth.User"},
    ],

    # ── User menu ───────────────────────────────
    "usermenu_links": [
        {"name": "Ver site", "url": "/", "new_window": False},
        {"model": "auth.User"},
    ],

    # ── Sidebar ─────────────────────────────────
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [
        "jogos",
        "accounts",
        "auth",
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "accounts.Perfil": "fas fa-id-card",
        "jogos.Jogo": "fas fa-gamepad",
        "jogos.Genero": "fas fa-tags",
        "jogos.Plataforma": "fas fa-desktop",
        "jogos.Avaliacao": "fas fa-star",
        "jogos.ItemListaDesejo": "fas fa-heart",
        "jogos.Conquista": "fas fa-trophy",
        "jogos.SessaoJogo": "fas fa-clock",
        "jogos.Notificacao": "fas fa-bell",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # ── UI ──────────────────────────────────────
    "related_modal_active": True,
    "custom_css": "css/admin_gamevault.css",
    "custom_js": None,
    "use_google_fonts_cdn": False,
    "show_ui_builder": False,

    # ── Tabs em formulários ─────────────────────
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },

    # ── Language chooser ────────────────────────
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-indigo",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-indigo",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
    "actions_sticky_top": True,
}
