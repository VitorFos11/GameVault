"""Lista tabelas do db.sqlite3 do GameVault (mesmo arquivo que o DBeaver usa)."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "db.sqlite3"
conn = sqlite3.connect(DB)
tables = [
    r[0]
    for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
]
print(f"Banco: {DB}")
print(f"Tabelas: {len(tables)}\n")
for name in tables:
    n = conn.execute(f"SELECT COUNT(*) FROM [{name}]").fetchone()[0]
    print(f"  {name:40} {n:6} linhas")
conn.close()
