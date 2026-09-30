# Capturas para o README (GameVault v2)

Inspirado no [ProLobby](https://github.com/ljborgess/ProLobby.com) (branch `dev`), seção **As telas**.

## Arquivos esperados

Salve PNG ou JPG (largura ~1400px) nesta pasta:

| Arquivo | URL (com `runserver`) | Conteúdo |
|---------|------------------------|----------|
| `01-landing.png` | `/` | Landing pública |
| `02-login.png` | `/conta/login/` | Login |
| `03-registro.png` | `/conta/registro/` | Criar conta |
| `04-dashboard.png` | `/dashboard/` | Dashboard + gráficos |
| `05-biblioteca.png` | `/biblioteca/` | Biblioteca (grade) |
| `06-detalhe.png` | `/jogo/<id>/` | Detalhe do jogo |
| `07-formulario.png` | `/novo/` | Cadastro de jogo |
| `08-wishlist.png` | `/lista-desejos/` | Wishlist |
| `09-perfil.png` | `/conta/perfil/` | Perfil |

## Como capturar (manual)

```powershell
.\venv\Scripts\activate
python manage.py runserver
```

Use **Win + Shift + S** (ou similar) em cada URL. Conta demo local: `demo` / `demo123456` (se criada).

## Automático (opcional)

Com Playwright instalado (`pip install playwright` + `python -m playwright install chromium`):

```powershell
python scripts/capture_screenshots.py
```

Depois atualize o README se renomear arquivos.
