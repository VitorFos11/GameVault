# Ver o banco GameVault (alternativa ao DBeaver)

No **Windows**, o DBeaver 26 usa **Java 25** e o driver SQLite às vezes **não carrega a DLL nativa**, mesmo com o arquivo correto. O banco **funciona** no Django; só a ferramenta JDBC falha.

Use o **DB Browser for SQLite** — abre o mesmo `db.sqlite3`, sem driver Java.

## Instalar

1. Baixe: [https://sqlitebrowser.org/dl/](https://sqlitebrowser.org/dl/) → **Windows** → instalador standard.
2. Instale e abra.

## Abrir o GameVault

1. **Arquivo** → **Abrir banco de dados…**
2. Selecione na **raiz do projeto**:

```text
...\GameVault\db.sqlite3
```

(Ex.: `C:\Users\...\OneDrive\...\GameVault\db.sqlite3` — o arquivo pode aparecer como `db` se as extensões estiverem ocultas.)

3. Aba **Estrutura do banco** → tabelas `jogos_jogo`, `jogos_genero`, `auth_user`, etc.
4. Aba **Procurar dados** → escolha a tabela → ver linhas.
5. Aba **Executar SQL** → cole as queries de [`dbeaver_apresentacao.sql`](dbeaver_apresentacao.sql).

## Apresentação (site + banco)

1. Cadastre usuário/jogo no site.
2. No DB Browser: **Executar SQL** → `SELECT COUNT(*) FROM jogos_jogo;` ou F5 na aba de dados da tabela.
3. Os números batem com o dashboard (mesmo arquivo que o `runserver` usa).

## DBeaver depois

Se no futuro o DBeaver conectar, use o mesmo caminho `db.sqlite3`. Até lá, o DB Browser atende a entrega acadêmica (visualizar tabelas, SQL, relações).
