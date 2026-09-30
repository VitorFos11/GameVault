# GameVault — Banco de dados e DBeaver

## SQLite (desenvolvimento local)

1. Execute migrations: `python manage.py migrate`
2. O arquivo fica em `db.sqlite3` na raiz do projeto.
3. No **DBeaver**: *Database* → *New Database Connection* → **SQLite** → selecione `db.sqlite3`.

## PostgreSQL (opcional)

1. Suba o banco: `docker compose up -d db`
2. No `.env`, defina:
   `DATABASE_URL=postgres://gamevault:gamevault@localhost:5432/gamevault`
3. Instale driver: `pip install psycopg2-binary`
4. Rode `python manage.py migrate`
5. No **DBeaver**: nova conexão **PostgreSQL** — host `localhost`, porta `5432`, database `gamevault`, usuário/senha `gamevault`.

## Tabelas principais

| Tabela | Descrição |
|--------|-----------|
| `jogos_jogo` | Biblioteca de jogos |
| `jogos_genero` | Gêneros |
| `jogos_plataforma` | Plataformas |
| `jogos_avaliacao` | Reviews por usuário |
| `jogos_itemlistadesejo` | Wishlist |
| `jogos_conquista` | Achievements |
| `jogos_sessaojogo` | Sessões de jogo |
| `accounts_perfil` | Perfil estendido |

Nunca commite `db.sqlite3` com dados sensíveis se o repositório for público.
