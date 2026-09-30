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



Plataforma **Django** para gerenciar coleção pessoal de jogos: **dashboard** com indicadores do banco, **biblioteca** com busca e filtros, **wishlist**, **avaliações**, **conquistas**, **catálogo** de gêneros e plataformas, **estatísticas** e **perfil** — interface **dark SaaS** (sidebar, topbar, tema claro/escuro, logo SVG).



Entrega acadêmica: **quatro tabelas de domínio** (`Gênero`, `Plataforma`, `Jogo`, `Avaliação`) com **1:N** (gênero→jogo, jogo→avaliação) e **N:N** (jogo↔plataforma), **CRUD** completo e conferência no **`db.sqlite3`** (DBeaver ou DB Browser for SQLite).



---



## Como funciona



| Etapa | O que você faz |

|-------|----------------|

| **1. Conta** | Registro em `/conta/registro/` — biblioteca por usuário (jogos compartilhados sem dono também aparecem) |

| **2. Catálogo** | CRUD de **gêneros** e **plataformas** (sidebar → Catálogo) |

| **3. Biblioteca** | **+ Jogo** no topo: cadastro, capa, status, progresso, plataformas (checkboxes) |

| **4. Dashboard** | Totais, preços, distribuição por gênero/plataforma — dados reais do ORM |

| **5. Detalhe** | Avaliação, sessões, conquistas, wishlist, painel de relacionamentos |

| **6. Apresentação** | Cadastre no site → atualize o **`db.sqlite3`** no DBeaver ou DB Browser |

| **7. Extra** | Admin Jazzmin, PostgreSQL opcional via `.env` |



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

| DBeaver: native library (Windows) | [docs/DATABASE_DBEAVER.md](docs/DATABASE_DBEAVER.md) ou [DB Browser](docs/DB_BROWSER_SQLITE.md) |



---



## Rotas principais



| Página | URL |

|--------|-----|

| Landing | `/` |

| Registro / Login | `/conta/registro/` · `/conta/login/` |

| Dashboard | `/dashboard/` |

| Biblioteca | `/biblioteca/` |

| Wishlist | `/lista-desejos/` |

| Estatísticas | `/estatisticas/` |

| Configurações | `/configuracoes/` |

| Gêneros (CRUD) | `/generos/` |

| Plataformas (CRUD) | `/plataformas/` |

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

| `DATABASE_URL` | PostgreSQL; **vazio = SQLite** (`db.sqlite3`) |

| `GAMES_PER_PAGE` | Paginação (padrão `12`) |



Não há chaves de API externa — cadastro de jogos é **manual** pelo site.



---



## Banco de dados



| Ambiente | Onde |

|----------|------|

| **SQLite (padrão)** | Arquivo `db.sqlite3` na raiz, após `migrate` |

| **Visualizar (SQLite)** | Arquivo `db.sqlite3` na **raiz** (sem host/senha). DBeaver: campo **Path** · DB Browser: **Abrir banco de dados** |

| **Conferência terminal** | `python scripts/list_db_tables.py` |

| **DBeaver (Windows)** | `powershell -ExecutionPolicy Bypass -File scripts/setup_dbeaver_sqlite_native.ps1` (driver 3.44 + DLL) |



Documentação:



- [docs/DATABASE_DBEAVER.md](docs/DATABASE_DBEAVER.md) — DBeaver, ER, apresentação ao vivo

- [docs/DB_BROWSER_SQLITE.md](docs/DB_BROWSER_SQLITE.md) — alternativa estável no Windows

- [docs/dbeaver_conexao_pronta.md](docs/dbeaver_conexao_pronta.md) — checklist de conexão

- [docs/dbeaver_apresentacao.sql](docs/dbeaver_apresentacao.sql) — queries para demo



**PostgreSQL (opcional):** `docker compose up -d db`, `DATABASE_URL=postgres://gamevault:gamevault@localhost:5432/gamevault` no `.env`, depois `migrate`.



### Tabelas de domínio (SQLite)



| Modelo | Tabela | Relação |

|--------|--------|---------|

| Gênero | `jogos_genero` | 1:N → `jogos_jogo` |

| Plataforma | `jogos_plataforma` | N:N via `jogos_jogo_plataformas` |

| Jogo | `jogos_jogo` | 1:N → `jogos_avaliacao` |

| Avaliação | `jogos_avaliacao` | FK para jogo e usuário |



---



## Testes



```bash

python manage.py test jogos

```



---



## Estrutura



```

gamevault/     settings, URLs, admin Jazzmin

accounts/      auth, perfil, registro

jogos/         models, views, forms, stats, migrations

templates/     layout, biblioteca, catálogo, dashboard

static/        CSS, logo, JS

docs/          DBeaver, SQL de apresentação, capturas

scripts/       utilitários (ex.: list_db_tables.py)

db.sqlite3     banco demo versionado (SQLite local)

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


