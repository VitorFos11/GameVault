# GameVault — Banco de dados e DBeaver

O schema nasce nos models do Django. O DBeaver serve para **ler**, gerar o diagrama ER e conferir os números do dashboard. Não altere estrutura por `CREATE`/`ALTER`/`DROP` no DBeaver.

**Conexão já preparada neste PC:** leia [dbeaver_conexao_pronta.md](dbeaver_conexao_pronta.md) (fechar e reabrir o DBeaver após ajustes).

## Qual banco o GameVault está usando?

| Situação | Tipo | Host / senha no DBeaver? |
|---|---|---|
| Você roda `runserver` na pasta do projeto e **não** tem `DATABASE_URL` no `.env` | **SQLite** | **Não.** Só o **caminho do arquivo** `db.sqlite3`. |
| Você definiu `DATABASE_URL=postgres://...` no `.env` ou usa `docker compose` com Postgres | **PostgreSQL** | **Sim.** Host, porta, database, usuário e senha (abaixo). |

Se o assistente de conexão pede **Host**, **Porta** e **Senha**, você provavelmente escolheu **PostgreSQL** ou **MySQL**. Para o dia a dia do projeto (arquivo `db.sqlite3` na raiz), escolha **SQLite**.

---

## SQLite (padrão — sem host e sem senha)

1. Confirme: na raiz do projeto existe `db.sqlite3` (se não, `python manage.py migrate`).
2. DBeaver: **Banco de dados** → **Nova conexão de banco de dados** (`Ctrl+Shift+N`).
3. Na lista, selecione **SQLite** (não PostgreSQL) → **Avançar** / **Next**.
4. Aba **Principal** / **Main**:
   - **Path** / **Caminho**: clique em **Browse** e escolha o arquivo:

```text
C:\Users\HOME\OneDrive\Desktop\Game_Valte\GameVault\db.sqlite3
```

   - Deixe **User** / **Password** em branco (SQLite não usa login).
5. **Testar conexão…** — na 1ª vez o DBeaver baixa o driver; aguarde e teste de novo.
6. **Concluir** / **Finish**.
7. No painel **Conexões**, expanda a conexão → **Tables** → você deve ver `jogos_jogo`, `auth_user`, etc.

**Nome da conexão:** pode ser `GameVault SQLite` para achar fácil na apresentação.

**Script SQL:** no editor, troque **N/A** pelo nome dessa conexão no dropdown acima do texto SQL.

Deixe o editor em auto-commit. Transação aberta no DBeaver trava o SQLite e o `runserver` passa a falhar ao salvar.

### Erro: `No native library found for os.name=Windows, os.arch=x86_64`

O driver **sqlite-jdbc** precisa extrair uma DLL nativa para uma pasta temporária. No Windows isso falha se o driver não baixou direito ou se a pasta temp bloqueia execução (OneDrive, antivírus, política da empresa).

**Tente nesta ordem:**

1. **Atualizar o driver SQLite**
   - **Banco de dados** → **Gerenciador de drivers** / **Driver Manager**.
   - Selecione **SQLite** → **Editar** / **Edit**.
   - Aba **Bibliotecas** / **Libraries** → **Baixar/Atualizar** / **Download/Update** (precisa de internet; desligue VPN/proxy se falhar).
   - **OK** → teste a conexão de novo.

2. **Pasta temp só para o SQLite (solução que mais funciona no Windows)**
   - Feche o DBeaver.
   - Crie uma pasta, por exemplo: `C:\Users\HOME\DBeaver\sqlite-tmp` (permissão total para seu usuário).
   - Abra o `dbeaver.ini` na pasta de instalação do DBeaver (ex.: `C:\Users\HOME\AppData\Local\DBeaver\dbeaver.ini` ou onde o instalador colocou o programa).
   - Logo **depois** da linha `-vmargs`, adicione:

```ini
-Dorg.sqlite.tmpdir=C:\Users\HOME\DBeaver\sqlite-tmp
```

   - Salve, abra o DBeaver de novo e **Testar conexão**.

3. **Se ainda falhar**, na mesma seção `-vmargs` do `dbeaver.ini`, acrescente também:

```ini
-Djava.io.tmpdir=C:\Users\HOME\DBeaver\sqlite-tmp
```

4. **Driver manual** (sem Maven): baixe [sqlite-jdbc](https://github.com/xerial/sqlite-jdbc/releases) (jar **with native** para Windows), em **Driver Manager → SQLite → Libraries → Add File** aponte o `.jar`, depois teste.

5. **Alternativa para a apresentação:** use **DB Browser for SQLite** apontando para o mesmo `db.sqlite3`, ou instale PostgreSQL via Docker e use as credenciais da seção PostgreSQL abaixo (exige `DATABASE_URL` no `.env` e `migrate`).

Referência: [DBeaver issue #13793](https://github.com/dbeaver/dbeaver/issues/13793).

### Erro: `NativeDB._open_utf8` / *No native library found* / *Unexpected driver error*

Causa: o driver **sqlite-jdbc** não carrega a DLL (temp bloqueada, antivírus ou **Java 25** do DBeaver 26 com JDBC 3.53+).

**Correção recomendada (script + driver 3.44.1.0):**

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_dbeaver_sqlite_native.ps1
```

Feche e reabra o DBeaver. O script baixa **sqlite-jdbc 3.44.1.0**, copia para a pasta de drivers do DBeaver e extrai `sqlitejdbc.dll`.

No `dbeaver.ini` (**depois** de `-vmargs`), deve existir algo como:

```ini
-Dorg.sqlite.tmpdir=C:\Users\HOME\DBeaver\sqlite-tmp
-Djava.io.tmpdir=C:\Users\HOME\DBeaver\sqlite-tmp
-Dorg.sqlite.lib.path=C:/Users/HOME/DBeaver/sqlite-native-344/org/sqlite/native/Windows/x86_64
-Dorg.sqlite.lib.name=sqlitejdbc
```

**Não** use `-Djava.library.path` no `dbeaver.ini` — isso impede o DBeaver de carregar a interface (SWT) e o programa nem abre.

No projeto, rode (PowerShell, DBeaver **fechado**):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_dbeaver_sqlite_native.ps1
```

Reabra o DBeaver e teste a conexão SQLite com o **Path**:

`C:\Users\HOME\OneDrive\Desktop\Game_Valte\GameVault\db.sqlite3`

### Ligar o script SQL à conexão

No editor, o dropdown ao lado do nome do script não pode ficar em **N/A**: escolha a conexão do `db.sqlite3`.  
Arquivo pronto para a apresentação: [`dbeaver_apresentacao.sql`](dbeaver_apresentacao.sql) (importe em **Arquivos → Scripts** ou abra e cole no editor).

## Apresentação ao vivo (site + DBeaver)

Objetivo: mostrar que **cada cadastro no GameVault grava no mesmo arquivo** `db.sqlite3` que o DBeaver lê.

### Antes de começar

1. Terminal: `python manage.py runserver` (projeto aberto no navegador).
2. DBeaver: conexão SQLite apontando para o **mesmo** `db.sqlite3` da raiz do projeto.
3. **Auto-commit ligado** (ícone de commit na toolbar; não deixe transação aberta).
4. Deixe o DBeaver visível ao lado do navegador (ou alterne com **F5** na tabela após cada ação).

### O que abrir no DBeaver durante a demo

| Ação no site | Onde ver no DBeaver | Tabela SQLite |
|---|---|---|
| Registro `/conta/registro/` | **Tables → auth_user → Dados** | `auth_user` |
| Perfil (avatar/bio) | `accounts_perfil` | `accounts_perfil` |
| Catálogo → **Gêneros** → novo | `jogos_genero` | `jogos_genero` |
| Catálogo → **Plataformas** → nova | `jogos_plataforma` | `jogos_plataforma` |
| **+ Jogo** (topbar) | `jogos_jogo` + `jogos_jogo_plataformas` | FK `genero_id`, N:N plataformas |
| Detalhe do jogo → **avaliação** | `jogos_avaliacao` | `jogo_id`, `usuario_id`, `nota` |
| **Wishlist** | `jogos_itemlistadesejo` | usuário + jogo |
| **Dashboard** (totais) | Query de contagem (abaixo) | deve coincidir com os `COUNT(*)` |

Atualizar dados na grade: botão direito na tabela → **Atualizar** ou **F5**.  
Se a linha não aparecer: confira se o caminho do arquivo no DBeaver é o da pasta do projeto (OneDrive às vezes abre outra cópia).

### Roteiro sugerido (5–8 min)

1. Rodar a query de **totais** (seção Consultas) e anotar os números; abrir o **Dashboard** e mostrar que batem.
2. Cadastrar um **gênero** → F5 em `jogos_genero` → contagem +1.
3. Cadastrar uma **plataforma** → F5 em `jogos_plataforma`.
4. **+ Jogo** preenchendo gênero e plataformas → F5 em `jogos_jogo` (nova linha) e em `jogos_jogo_plataformas` (vínculos N:N).
5. Abrir o jogo → salvar **avaliação** → F5 em `jogos_avaliacao`.
6. (Opcional) Criar usuário em **Registro** → F5 em `auth_user`.
7. Rodar de novo a query de totais e o bloco **1:N / N:N** para fechar com cardinalidade.

Script com queries “últimos registros”: [`dbeaver_apresentacao.sql`](dbeaver_apresentacao.sql).

### Problemas na hora H

| Sintoma | Solução |
|---|---|
| `database is locked` | Fechar abas de edição no DBeaver, desligar transação manual, parar e subir o `runserver` de novo. |
| Site salva, DBeaver não muda | Atualizar tabela (F5); reexecutar o `SELECT`; verificar caminho do `.sqlite3`. |
| Contagem diferente do Dashboard | Dashboard usa a biblioteca do usuário logado; `COUNT(*)` em `jogos_jogo` é **global** (todos os jogos). Explique ou filtre `WHERE usuario_id = …`. |

## PostgreSQL (opcional — só se usar Docker ou DATABASE_URL)

Use esta seção **apenas** se o Django também estiver apontando para Postgres (`.env` com `DATABASE_URL`). Senão o DBeaver mostraria um banco **diferente** do site.

1. `docker compose up -d db`
2. No `.env`: `DATABASE_URL=postgres://gamevault:gamevault@localhost:5432/gamevault`
3. `pip install psycopg2-binary` e `python manage.py migrate`
4. DBeaver: **Nova conexão** → **PostgreSQL** → preencha:

| Campo DBeaver | Valor |
|---|---|
| Host | `localhost` |
| Porta | `5432` |
| Database | `gamevault` |
| Usuário | `gamevault` |
| Senha | `gamevault` |

5. **Testar conexão** → **Concluir**.

(O `docker-compose.yml` do projeto usa exatamente esses valores em `POSTGRES_*`.)

## As quatro tabelas da atividade

| Tabela Django | Tabela no SQLite | Papel |
|---|---|---|
| `Genero` | `jogos_genero` | Catálogo de gêneros |
| `Plataforma` | `jogos_plataforma` | Catálogo de plataformas |
| `Jogo` | `jogos_jogo` | Biblioteca (CRUD principal) |
| `Avaliacao` | `jogos_avaliacao` | Notas e comentários |

Junções do ORM (não contam como “modelo extra” na apresentação):

- `jogos_jogo_plataformas` — JOGO N:N PLATAFORMA
- `jogos_jogo_generos` — gêneros extras (o gênero principal é FK)

Para **demonstrar cadastro de usuário**, use `auth_user` (e `accounts_perfil` se editar perfil).  
Não entrar no slide das “quatro tabelas”: `django_*`, `sessions`, `contenttypes`.

### Cardinalidades

```
GENERO 1 ---- N JOGO          (jogos_jogo.genero_id, ON DELETE PROTECT)
JOGO   1 ---- N AVALIACAO     (jogos_avaliacao.jogo_id, ON DELETE CASCADE)
JOGO   N ---- N PLATAFORMA    (tabela jogos_jogo_plataformas)
```

Há **pelo menos uma** relação 1:N (`Genero` → `Jogo` e `Jogo` → `Avaliacao`).

## Consultas de conferência (colar no editor SQL do DBeaver)

```sql
-- Totais das quatro tabelas
SELECT 'genero' AS tabela, COUNT(*) AS registros FROM jogos_genero
UNION ALL SELECT 'plataforma', COUNT(*) FROM jogos_plataforma
UNION ALL SELECT 'jogo', COUNT(*) FROM jogos_jogo
UNION ALL SELECT 'avaliacao', COUNT(*) FROM jogos_avaliacao;

-- GENERO 1:N JOGO
SELECT g.nome AS genero, COUNT(j.id) AS jogos
FROM jogos_genero g
LEFT JOIN jogos_jogo j ON j.genero_id = g.id
GROUP BY g.id, g.nome
ORDER BY jogos DESC, genero;

-- JOGO 1:N AVALIACAO
SELECT j.nome AS jogo, COUNT(a.id) AS avaliacoes, ROUND(AVG(a.nota), 2) AS media
FROM jogos_jogo j
LEFT JOIN jogos_avaliacao a ON a.jogo_id = j.id
GROUP BY j.id, j.nome
ORDER BY avaliacoes DESC, jogo;

-- JOGO N:N PLATAFORMA
SELECT p.nome AS plataforma, COUNT(jp.jogo_id) AS jogos
FROM jogos_plataforma p
LEFT JOIN jogos_jogo_plataformas jp ON jp.plataforma_id = p.id
GROUP BY p.id, p.nome
ORDER BY jogos DESC, plataforma;

-- Indicadores do dashboard
SELECT COUNT(*) AS total_jogos,
       ROUND(AVG(preco), 2) AS preco_medio,
       MAX(preco) AS maior_preco,
       MIN(preco) AS menor_preco
FROM jogos_jogo;
```

O diagrama ER: botão direito em `Tables` → `Ver Diagrama`, ou pasta `Diagrams` → novo diagrama só com as quatro tabelas e as duas junções.

Nunca commite `db.sqlite3` com dados sensíveis se o repositório for público.
