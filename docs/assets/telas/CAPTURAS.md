# Capturas para o README (GameVault v2)

## Arquivos

| Arquivo | URL (`runserver 8765`) | Conteúdo |
|---------|------------------------|----------|
| `01-landing.png` | `/` | Landing pública |
| `02-login.png` | `/conta/login/` | Login |
| `04-dashboard.png` | `/dashboard/` | Dashboard acadêmico |
| `05-biblioteca.png` | `/biblioteca/` | Minha biblioteca (entradas do usuário) |
| `06-detalhe.png` | `/jogo/<id>/` | Detalhe do jogo |
| `07-formulario.png` | `/novo/` | Cadastro de jogo (**staff_demo**) |
| `13-explorar.png` | `/explorar/` | Explorar catálogo global |
| `08-wishlist.png` | `/lista-desejos/` | Wishlist |
| `09-perfil.png` | `/conta/perfil/` | Perfil |
| `10-estatisticas.png` | `/estatisticas/` | Estatísticas + gráficos |
| `11-catalogo-generos.png` | `/generos/` | CRUD de gêneros |
| `12-configuracoes.png` | `/configuracoes/` | Tema + sair / trocar usuário |

## Automático (Playwright)

Terminal 1:

```powershell
.\venv\Scripts\activate
python manage.py runserver 8765
```

Terminal 2:

```powershell
.\venv\Scripts\activate
pip install playwright
python -m playwright install chromium
python scripts/capture_screenshots.py
```

Contas: **`demo`** / **`demo123456`** (usuário comum; biblioteca preenchida com jogos do catálogo) e **`staff_demo`** / **`demo123456`** (só para `07-formulario.png`).

## Manual

`Win + Shift + S` em cada URL com o servidor em **http://127.0.0.1:8000/** (ou 8765). Salve PNG ~1400px de largura nesta pasta.
