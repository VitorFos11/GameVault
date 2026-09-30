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

Plataforma **Django** para gerenciar sua coleção pessoal de jogos: dashboard com métricas reais, biblioteca com filtros, wishlist, avaliações, conquistas e perfil — interface **dark SaaS** com sidebar, tema claro/escuro e identidade GameVault (logo SVG).

---

## Como funciona

| Etapa | O que você faz |
|-------|----------------|
| **1. Conta** | Registro em `/conta/registro/` — cada usuário vê só a própria biblioteca |
| **2. Biblioteca** | Cadastro, capa, status (jogando, backlog, concluído…), progresso e horas |
| **3. Dashboard** | Totais, gráficos por plataforma/gênero/status — tudo vindo do banco |
| **4. Detalhe** | Review, sessões de jogo, conquistas, wishlist rápida |
| **5. Extra** | Importação RAWG (opcional), admin Django, PostgreSQL via `.env` |

---

## As telas

Capturas da **v2** ficam em [`docs/assets/telas/`](docs/assets/telas/CAPTURAS.md) (mesmo padrão do [ProLobby](https://github.com/ljborgess/ProLobby.com/tree/dev)).  
Gere com o servidor local e o guia **[CAPTURAS.md](docs/assets/telas/CAPTURAS.md)** ou `python scripts/capture_screenshots.py` (Playwright).

### v2 (adicione os arquivos abaixo)

| | |
|---|---|
| ![Landing](docs/assets/telas/01-landing.png) | ![Dashboard](docs/assets/telas/04-dashboard.png) |
| **Landing** | **Dashboard** |
| ![Biblioteca](docs/assets/telas/05-biblioteca.png) | ![Detalhe](docs/assets/telas/06-detalhe.png) |
| **Biblioteca** | **Detalhe do jogo** |
| ![Formulário](docs/assets/telas/07-formulario.png) | ![Perfil](docs/assets/telas/09-perfil.png) |
| **Cadastro / edição** | **Perfil** |

> Até as capturas v2 existirem, o GitHub pode mostrar ícones quebrados nesta tabela — isso é esperado. Siga [CAPTURAS.md](docs/assets/telas/CAPTURAS.md).

### Referência visual (v1 — histórico do projeto)

| | |
|---|---|
| ![Início v1](images/home.png) | ![Cadastro v1](images/cadastro.png) |
| **Catálogo inicial** | **Formulário de jogo** |
| ![Pesquisa v1](images/pesquisa.png) | ![Detalhe v1](images/ver.png) |
| **Busca** | **Visualização** |

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

Abra **http://127.0.0.1:8000/** → **Criar conta** ou login.

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

---

## Rotas principais

| Página | URL |
|--------|-----|
| Landing | `/` |
| Registro / Login | `/conta/registro/` · `/conta/login/` |
| Dashboard | `/dashboard/` |
| Biblioteca | `/biblioteca/` |
| Wishlist | `/lista-desejos/` |
| Novo jogo | `/novo/` |
| Admin | `/admin/` |

---

## Variáveis de ambiente

Arquivo [.env.example](.env.example):

| Variável | Uso |
|----------|-----|
| `SECRET_KEY` | Django (troque em produção) |
| `DEBUG` | `True` em dev |
| `DATABASE_URL` | PostgreSQL; vazio = SQLite |
| `RAWG_API_KEY` | Busca externa em Importar |
| `GAMES_PER_PAGE` | Paginação (padrão `12`) |

---

## Banco de dados

- **SQLite:** `db.sqlite3` após `migrate`
- **DBeaver:** [docs/DATABASE_DBEAVER.md](docs/DATABASE_DBEAVER.md)
- **Docker:** `docker compose up -d db` + `DATABASE_URL` no `.env`

---

## Testes

```bash
python manage.py test jogos
```

---

## Estrutura

```
gamevault/     settings, URLs
accounts/      auth e perfil
jogos/         models, views, services
templates/     layout e páginas
static/        CSS, logo, JS
docs/          DBeaver, capturas README
```

---

## Design e Figma

Para alinhar telas a um layout Figma no Cursor, use **Agent** + skill **Figma design-to-code** com o link do frame (ex.: `https://www.figma.com/design/...`).  
Prompt sugerido:

> GameVault — dark SaaS, sem gradientes exagerados, sidebar + dashboard; altere só `static/css` e `templates/`.

Modelos fortes para **UI/front-end**: Claude **Opus** ou **Sonnet (thinking)** no Agent; ajustes rápidos com **Composer**.

---

## Créditos

**GameVault v2.0** — 2026  

**Vitor Faria de Oliveira e Silva** · **Rafael Junqueira de Souza**

Projeto acadêmico / portfólio — Python e Django.
