<p align="center">
  <img src="static/img/logo-full.svg" alt="GameVault" width="280">
</p>

<p align="center">
  <strong>Sua biblioteca de jogos. Seu progresso. Seu vault.</strong><br>
  Plataforma web para organizar, acompanhar e redescobrir sua coleção de jogos.
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.11+"></a>
  <a href="https://www.djangoproject.com/"><img src="https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django&logoColor=white" alt="Django 5.2"></a>
  <img src="https://img.shields.io/badge/SQLite-Local-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/PostgreSQL-Opcional-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <a href=".github/workflows/ci.yml"><img src="https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="CI"></a>
</p>

---

## Índice

- [Sobre](#sobre)
- [Funcionalidades](#funcionalidades)
- [Início rápido](#início-rápido)
- [Rotas principais](#rotas-principais)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Banco de dados e DBeaver](#banco-de-dados-e-dbeaver)
- [Docker (opcional)](#docker-opcional)
- [Testes](#testes)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Créditos](#créditos)

---

## Sobre

O **GameVault** é uma aplicação **Django** que evoluiu de um CRUD acadêmico para uma **plataforma pessoal de biblioteca de jogos**: dashboard com métricas reais, biblioteca com filtros, wishlist, avaliações, conquistas, perfil de usuário e identidade visual moderna (tema claro/escuro).

Ideal para portfólio, estudos de backend e uso pessoal.

---

## Funcionalidades

| Área | O que você pode fazer |
|------|------------------------|
| **Biblioteca** | CRUD de jogos, capa/banner, status, progresso, horas jogadas, tags |
| **Dashboard** | Cards e gráficos (Chart.js) calculados a partir do banco |
| **Busca e filtros** | Nome, dev, gênero, plataforma, status, ano, nota; grade ou lista |
| **Conta** | Registro, login, perfil com avatar |
| **Wishlist** | Prioridade, preço alvo/atual, notas |
| **Social pessoal** | Avaliações 1–5, conquistas, sessões de jogo, notificações |
| **Integração** | Camada RAWG opcional (`RAWG_API_KEY`) para busca externa |
| **Admin** | Painel Django configurado para todos os modelos |

---

## Início rápido

### Pré-requisitos

- **Python 3.11+**
- **Git**
- (Opcional) [DBeaver](https://dbeaver.io/) para inspecionar o banco

### Passo a passo — Windows (PowerShell)

```powershell
# 1. Clonar e entrar na pasta
git clone https://github.com/VitorFos11/GameVault.git
cd GameVault

# 2. Ambiente virtual
python -m venv venv
.\venv\Scripts\activate

# 3. Dependências
pip install -r requirements.txt

# 4. Configuração
copy .env.example .env

# 5. Banco e usuário admin (opcional)
python manage.py migrate
python manage.py createsuperuser

# 6. Servidor
python manage.py runserver
```

Abra no navegador: **http://127.0.0.1:8000/**

> **Primeiro acesso:** clique em **Criar conta** ou use o superusuário em `/conta/login/`.

### Passo a passo — Linux / macOS

```bash
git clone https://github.com/VitorFos11/GameVault.git
cd GameVault
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser   # opcional
python manage.py runserver
```

### Problemas comuns

| Sintoma | Solução |
|---------|---------|
| `No module named 'django'` | Ative o `venv` e rode `pip install -r requirements.txt` novamente |
| Erro de SSL no `pip` (Windows) | `pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org` |
| Porta 8000 ocupada | `python manage.py runserver 8080` |
| Página pede login | `/conta/registro/` ou login com superusuário |

---

## Rotas principais

| Página | URL |
|--------|-----|
| Landing | http://127.0.0.1:8000/ |
| Registro | http://127.0.0.1:8000/conta/registro/ |
| Login | http://127.0.0.1:8000/conta/login/ |
| Dashboard | http://127.0.0.1:8000/dashboard/ |
| Biblioteca | http://127.0.0.1:8000/biblioteca/ |
| Wishlist | http://127.0.0.1:8000/lista-desejos/ |
| Novo jogo | http://127.0.0.1:8000/novo/ |
| Admin Django | http://127.0.0.1:8000/admin/ |

Rotas legadas da v1 (`/lista/`, etc.) continuam redirecionando ou apontando para a biblioteca.

---

## Variáveis de ambiente

Copie [.env.example](.env.example) para `.env`:

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `SECRET_KEY` | Chave Django | valor de dev (troque em produção) |
| `DEBUG` | Modo debug | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos | `127.0.0.1,localhost` |
| `DATABASE_URL` | PostgreSQL (vazio = SQLite) | — |
| `RAWG_API_KEY` | API RAWG para importação | vazio |
| `GAMES_PER_PAGE` | Paginação da biblioteca | `12` |

Nunca commite o arquivo `.env` com segredos reais.

---

## Banco de dados e DBeaver

- **Desenvolvimento:** SQLite em `db.sqlite3` (criado após `migrate`).
- **Produção / análise:** PostgreSQL via `DATABASE_URL`.

Guia detalhado de conexão no DBeaver: **[docs/DATABASE_DBEAVER.md](docs/DATABASE_DBEAVER.md)**

---

## Docker (opcional)

PostgreSQL local para testes:

```bash
docker compose up -d db
```

No `.env`:

```env
DATABASE_URL=postgres://gamevault:gamevault@localhost:5432/gamevault
```

Instale o driver: `pip install psycopg2-binary`, depois `python manage.py migrate`.

---

## Testes

```bash
python manage.py test jogos
```

O pipeline **CI** (`.github/workflows/ci.yml`) executa migrate, `check` e testes em cada pull request.

---

## Estrutura do projeto

```
GameVault/
├── gamevault/          # Settings, URLs raiz
├── accounts/           # Autenticação e perfil
├── jogos/              # Domínio principal (models, views, services)
├── templates/          # Layout (sidebar, dashboard, biblioteca…)
├── static/             # CSS modular, logo SVG, JavaScript
├── docs/               # Documentação (DBeaver)
├── media/              # Uploads (capas, avatares)
├── .env.example
├── requirements.txt
└── manage.py
```

---

## Créditos

**GameVault v2.0** — 2026

- **Vitor Faria de Oliveira e Silva**
- **Rafael Junqueira de Souza**

Projeto acadêmico / portfólio — Backend com **Python** e **Django**.

---

<p align="center">
  <sub>GameVault — organize, acompanhe, jogue.</sub>
</p>
