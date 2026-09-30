# DBeaver — conexão GameVault (já configurada no seu PC)

Foi feita configuração automática no seu Windows:

| Item | Valor |
|---|---|
| Arquivo do banco | `C:\Users\HOME\OneDrive\Desktop\Game_Valte\GameVault\db.sqlite3` |
| Conexão DBeaver | **GameVault (db.sqlite3)** (em `data-sources.json`) |
| Pasta temp SQLite | `C:\Users\HOME\DBeaver\sqlite-tmp` |
| Ajuste em | `%LOCALAPPDATA%\DBeaver\dbeaver.ini` (`-Dorg.sqlite.tmpdir` e `-Djava.io.tmpdir`) |

## O que você faz agora (2 minutos)

1. **Feche o DBeaver** completamente (se estiver aberto).
2. Abra o DBeaver de novo (para carregar o `dbeaver.ini` novo).
3. No painel **Conexões**, clique em **GameVault (db.sqlite3)**.
   - Se não aparecer: **Banco de dados** → **Nova conexão** → **SQLite** → caminho do `db.sqlite3` acima.
4. Botão direito na conexão → **Conectar** / duplo clique.
5. Expanda **Tables** — você verá **22 tabelas**, incluindo:
   - `auth_user` (usuários)
   - `jogos_jogo`, `jogos_genero`, `jogos_plataforma`, `jogos_avaliacao`
   - `jogos_jogo_plataformas` (N:N)

## Ver todo o banco

- **Tables** → duplo clique em uma tabela → aba **Dados**.
- Ou abra `docs/dbeaver_apresentacao.sql`, selecione a conexão **GameVault** (não N/A) e execute com **Ctrl+Enter**.

## Conferir pelo terminal (sem DBeaver)

```powershell
cd C:\Users\HOME\OneDrive\Desktop\Game_Valte\GameVault
.\venv\Scripts\python.exe scripts\list_db_tables.py
```

## Se ainda der erro de native library

1. DBeaver fechado → **Gerenciador de drivers** → **SQLite** → **Bibliotecas** → **Baixar/Atualizar**.
2. Ou **Add File** → JAR em  
   `%APPDATA%\DBeaverData\drivers\maven\maven-central\org.xerial\sqlite-jdbc-3.53.4.0.jar`  
   (deve existir após o download do Maven).

3. Reinicie o DBeaver.

## Importante

- **Não** use PostgreSQL para este projeto enquanto o `.env` não tiver `DATABASE_URL`.
- Host/senha **não se aplicam** ao SQLite.
