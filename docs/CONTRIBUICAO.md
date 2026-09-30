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
