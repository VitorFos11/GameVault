# GameVault v2.0

Plataforma moderna de biblioteca e acompanhamento de jogos — Django, design system dark/light, estatísticas dinâmicas, wishlist, reviews, conquistas e camada preparada para APIs externas (RAWG).

## Funcionalidades

- CRUD completo de jogos (capa, banner, progresso, status, tags)
- Dashboard com cards e gráficos (Chart.js) alimentados pelo banco
- Biblioteca com busca, filtros, ordenação, paginação, grade/lista
- Autenticação (registro, login, perfil, avatar)
- Wishlist com prioridade e preços alvo
- Avaliações pessoais (1–5), conquistas e sessões de jogo
- Notificações, importação via RAWG (com `RAWG_API_KEY`)
- Admin Django aprimorado
- SQLite local + suporte PostgreSQL via `DATABASE_URL`
- Documentação DBeaver: [docs/DATABASE_DBEAVER.md](docs/DATABASE_DBEAVER.md)

## Instalação rápida

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

## Variáveis de ambiente

Veja [.env.example](.env.example).

## Testes e CI

```bash
python manage.py test jogos
```

Workflow GitHub Actions em `.github/workflows/ci.yml`.

## Estrutura

```
gamevault/          # settings, urls
accounts/           # perfil e auth
jogos/              # models, views, services
templates/          # layout shell + páginas
static/             # CSS, JS, logo SVG
docs/               # DBeaver / banco
```

## Versão

**GameVault v2.0** — evolução do CRUD v1.0 mantendo compatibilidade de rotas (`/lista/`, `/novo/`, etc.).

Desenvolvido em 2026.
