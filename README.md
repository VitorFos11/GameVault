<div align="center">

# GameVault

**Sua biblioteca de jogos. Seu progresso. Seu vault.**

[![CI](https://github.com/VitorFos11/GameVault/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/VitorFos11/GameVault/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![Status](https://img.shields.io/badge/status-v2.0-6366f1)

<p align="center">
  <img src="static/img/logo-full.svg" alt="GameVault" width="300">
</p>

</div>

---

## Sobre

Plataforma **Django** para gerenciar coleção pessoal de jogos: **dashboard** com indicadores do banco, **biblioteca** com busca e filtros, **wishlist**, **avaliações**, **conquistas**, **catálogo** (gêneros e plataformas), **estatísticas** e **perfil**. Interface **dark SaaS** — sidebar, topbar, cards e tema claro/escuro.

**Entrega acadêmica:** quatro tabelas de domínio (`Gênero`, `Plataforma`, `Jogo`, `Avaliação`), relações **1:N** e **N:N**, **CRUD** completo e conferência no **`db.sqlite3`** (DBeaver ou [DB Browser for SQLite](docs/DB_BROWSER_SQLITE.md)).

---

## Como funciona

| Etapa | O que você faz |
|-------|----------------|
| **1. Conta** | Registro em `/conta/registro/` — biblioteca filtrada por usuário (+ jogos demo compartilhados sem dono) |
| **1b. Sessão** | **Sair** (sidebar, topbar ou Configurações) → volta ao login para entrar com outra conta |
| **2. Catálogo** | CRUD de gêneros e plataformas (menu lateral) |
| **3. Biblioteca** | **+ Jogo**: cadastro, capa, status, plataformas |
| **4. Dashboard** | Totais e distribuições calculados pelo ORM |
| **5. Detalhe** | Clique no jogo na biblioteca — avaliações, progresso, conquistas, wishlist |
| **6. Apresentação** | Cadastre no site → atualize `db.sqlite3` no DBeaver ou DB Browser |
| **7. Extra** | Admin Jazzmin · PostgreSQL opcional (`.env`) |

---

## As telas

Interface **v2** (sidebar, dashboard acadêmico, biblioteca em grade, catálogo e estatísticas).

| | |
|---|---|
| ![Landing](docs/assets/telas/01-landing.png) | ![Login](docs/assets/telas/02-login.png) |
| **Landing** | **Login** |
| ![Dashboard](docs/assets/telas/04-dashboard.png) | ![Biblioteca](docs/assets/telas/05-biblioteca.png) |
| **Dashboard** | **Biblioteca** |
| ![Detalhe](docs/assets/telas/06-detalhe.png) | ![Novo jogo](docs/assets/telas/07-formulario.png) |
| **Detalhe do jogo** | **Cadastro de jogo** |
| ![Estatísticas](docs/assets/telas/10-estatisticas.png) | ![Catálogo gêneros](docs/assets/telas/11-catalogo-generos.png) |
| **Estatísticas** | **Catálogo — gêneros** |
| ![Wishlist](docs/assets/telas/08-wishlist.png) | ![Perfil](docs/assets/telas/09-perfil.png) |
| **Wishlist** | **Perfil** |
| ![Configurações](docs/assets/telas/12-configuracoes.png) | |
| **Configurações e sessão** | |

Para regerar as capturas: [`docs/assets/telas/CAPTURAS.md`](docs/assets/telas/CAPTURAS.md) ou `python scripts/capture_screenshots.py` (com `runserver` na porta **8765**).

<details>
<summary>Referência visual v1 (layout antigo)</summary>

| | |
|---|---|
| ![Início v1](images/home.png) | ![Cadastro v1](images/cadastro.png) |
| **Catálogo inicial** | **Formulário** |
| ![Pesquisa v1](images/pesquisa.png) | ![Detalhe v1](images/ver.png) |
| **Busca** | **Visualização** |

</details>

---

## Começando

Requer **Python 3.11+** e **Git**.

### Windows (PowerShell)

```powershell
git clone https://github.com/VitorFos11/GameVault.git
cd GameVault
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser   # opcional
python manage.py runserver
```

Abra **http://127.0.0.1:8000/** → criar conta ou login.

**Conta demo (opcional):** `demo` / `demo123456` — o script `scripts/capture_screenshots.py` cria essa conta se ela não existir.

### Linux / macOS

```bash
git clone https://github.com/VitorFos11/GameVault.git && cd GameVault
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

### Problemas comuns

| Sintoma | Solução |
|---------|---------|
| `No module named 'django'` | Ative o `venv` e `pip install -r requirements.txt` |
| SSL no pip (Windows) | `--trusted-host pypi.org --trusted-host files.pythonhosted.org` |
| Porta ocupada | `python manage.py runserver 8080` |
| DBeaver: erro de DLL (Windows) | [DATABASE_DBEAVER.md](docs/DATABASE_DBEAVER.md) ou [DB_BROWSER_SQLITE.md](docs/DB_BROWSER_SQLITE.md) |

---

## Rotas principais

| Página | URL |
|--------|-----|
| Landing | `/` |
| Registro / Login / Sair | `/conta/registro/` · `/conta/login/` · sair (POST em `/conta/logout/`) |
| Dashboard | `/dashboard/` |
| Biblioteca | `/biblioteca/` |
| Wishlist | `/lista-desejos/` |
| Estatísticas | `/estatisticas/` |
| Configurações | `/configuracoes/` |
| Gêneros | `/generos/` |
| Plataformas | `/plataformas/` |
| Conquistas | `/conquistas/` |
| Novo jogo | `/novo/` |
| Perfil | `/conta/perfil/` |
| Admin | `/admin/` |

---

## Variáveis de ambiente

Arquivo [.env.example](.env.example):

| Variável | Uso |
|----------|-----|
| `SECRET_KEY` | Django (troque em produção) |
| `DEBUG` | `True` em dev |
| `DATABASE_URL` | PostgreSQL; vazio = SQLite (`db.sqlite3`) |
| `GAMES_PER_PAGE` | Paginação (padrão `12`) |

Cadastro de jogos é **manual** (sem API externa).

---

## Banco de dados

| Ambiente | Onde |
|----------|------|
| **SQLite (padrão)** | `db.sqlite3` na raiz, após `migrate` |
| **Visualizar** | Mesmo arquivo no DBeaver (**Path**) ou DB Browser (**Abrir banco**) |
| **Terminal** | `python scripts/list_db_tables.py` |
| **DBeaver (Windows)** | `scripts/setup_dbeaver_sqlite_native.ps1` |

Documentação: [DATABASE_DBEAVER.md](docs/DATABASE_DBEAVER.md) · [DB_BROWSER_SQLITE.md](docs/DB_BROWSER_SQLITE.md) · [dbeaver_apresentacao.sql](docs/dbeaver_apresentacao.sql)

**PostgreSQL (opcional):** `docker compose up -d db` + `DATABASE_URL=postgres://gamevault:gamevault@localhost:5432/gamevault` + `migrate`.

| Modelo | Tabela SQLite | Relação |
|--------|---------------|---------|
| Gênero | `jogos_genero` | 1:N → jogo |
| Plataforma | `jogos_plataforma` | N:N com jogo |
| Jogo | `jogos_jogo` | 1:N → avaliação |
| Avaliação | `jogos_avaliacao` | FK jogo + usuário |

---

## Testes

```bash
python manage.py test jogos accounts
```

---

## Estrutura

```
gamevault/     settings, URLs, admin Jazzmin
accounts/      auth, perfil, registro
jogos/         models, views, forms, stats
templates/     layout v2, catálogo, dashboard
static/        CSS, logo, JS
docs/          DBeaver, capturas, SQL de demo
scripts/       list_db_tables, capture_screenshots, setup DBeaver
db.sqlite3     banco demo (SQLite)
```

---

## Créditos

**GameVault v2.0** — 2026  

**Vitor Faria de Oliveira e Silva** · **Rafael Junqueira de Souza**

Projeto acadêmico / portfólio — Python e Django.
