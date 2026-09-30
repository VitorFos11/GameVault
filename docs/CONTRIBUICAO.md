# Contribuidores no GitHub

O repositório deve listar apenas:

- **Vitor Faria de Oliveira e Silva** (`VitorFos11` / `vitorfosanglo@gmail.com`)
- **Rafael Junqueira** (`rafaeljs08` / `rafaeljs08@hotmail.com`)

## Evitar Cursor como co-autor

O Cursor pode adicionar automaticamente ao final do commit:

```text
Co-authored-by: Cursor <cursoragent@cursor.com>
```

Isso faz o GitHub contar **Cursor** como contribuidor.

**Antes de commitar pelo Agent:** em **Cursor → Settings**, desative opções de incluir co-autor em commits (se existirem), ou revise a mensagem e remova a linha `Co-authored-by: Cursor` antes do push.

**Hook local (opcional):** copie um script `commit-msg` que rode `scripts/strip_cursor_coauthor.py` sobre a mensagem — assim commits feitos pelo Cursor no seu PC não levam o trailer.

## Corrigir histórico (já feito uma vez)

```powershell
git filter-branch -f --msg-filter "python C:/caminho/GameVault/scripts/strip_cursor_coauthor.py" -- --all
git push --force-with-lease origin main
```

Use `--force-with-lease` só quando todos combinarem (reescreve histórico).

O gráfico de contribuidores no GitHub pode levar **algumas horas** para atualizar após o force push.

## Sumir da barra lateral (Contributors)

1. **Branch remota `cursor/*` removida** — ela ainda tinha commits com `Co-authored-by: Cursor` e o GitHub contava o **cursoragent**.
2. No GitHub: **Insights → Contributors** → clique em **cursoragent** → confira se ainda lista commits. Se **0 commits**, é cache da barra lateral.
3. **Atualizar cache:** **Settings → General → Default branch** → renomeie `main` para `main-bkp`, salve; renomeie de volta para `main`. Aguarde 10–30 min.
4. (Opcional) **Settings da sua conta GitHub → Block user** → bloqueie `cursoragent` — some da contagem na sidebar mais rápido em alguns casos.
5. PRs antigos (#1) podem manter refs internas; isso **não** impede limpar a lista se `main` estiver limpo e branches `cursor/*` apagadas.
