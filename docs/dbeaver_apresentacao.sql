-- GameVault — script para apresentação no DBeaver
-- Conecte ao db.sqlite3 do projeto, execute um bloco por vez (Ctrl+Enter).
-- Depois de salvar no site, rode de novo ou F5 na aba Dados da tabela.

-- 1) Contagem rápida (deve bater com o Dashboard)
SELECT 'genero' AS tabela, COUNT(*) AS registros FROM jogos_genero
UNION ALL SELECT 'plataforma', COUNT(*) FROM jogos_plataforma
UNION ALL SELECT 'jogo', COUNT(*) FROM jogos_jogo
UNION ALL SELECT 'avaliacao', COUNT(*) FROM jogos_avaliacao
UNION ALL SELECT 'usuario', COUNT(*) FROM auth_user;

-- 2) Usuários (registro em /conta/registro/ ou Admin)
SELECT id, username, email, is_staff, date_joined
FROM auth_user
ORDER BY id DESC;

-- 3) Últimos jogos cadastrados (+ Jogo no site)
SELECT j.id, j.nome, g.nome AS genero, j.preco, j.status, j.usuario_id,
       datetime(j.criado_em) AS criado_em
FROM jogos_jogo j
JOIN jogos_genero g ON g.id = j.genero_id
ORDER BY j.id DESC
LIMIT 10;

-- 4) Plataformas ligadas ao jogo (N:N)
SELECT j.nome AS jogo, p.nome AS plataforma
FROM jogos_jogo j
JOIN jogos_jogo_plataformas jp ON jp.jogo_id = j.id
JOIN jogos_plataforma p ON p.id = jp.plataforma_id
ORDER BY j.id DESC, p.nome;

-- 5) Gêneros e plataformas do catálogo
SELECT id, nome, slug FROM jogos_genero ORDER BY id DESC LIMIT 10;
SELECT id, nome, slug FROM jogos_plataforma ORDER BY id DESC LIMIT 10;

-- 6) Avaliações (detalhe do jogo no site)
SELECT a.id, j.nome AS jogo, u.username, a.nota, a.comentario,
       datetime(a.criado_em) AS criado_em
FROM jogos_avaliacao a
JOIN jogos_jogo j ON j.id = a.jogo_id
JOIN auth_user u ON u.id = a.usuario_id
ORDER BY a.id DESC;

-- 7) Wishlist (opcional)
SELECT u.username, j.nome AS jogo, w.prioridade, datetime(w.criado_em) AS criado_em
FROM jogos_itemlistadesejo w
JOIN auth_user u ON u.id = w.usuario_id
JOIN jogos_jogo j ON j.id = w.jogo_id
ORDER BY w.id DESC;

-- 8) Relacionamentos 1:N e N:N (slides do professor)
SELECT g.nome AS genero, COUNT(j.id) AS jogos
FROM jogos_genero g
LEFT JOIN jogos_jogo j ON j.genero_id = g.id
GROUP BY g.id, g.nome
ORDER BY jogos DESC;

SELECT j.nome AS jogo, COUNT(a.id) AS avaliacoes, ROUND(AVG(a.nota), 2) AS media
FROM jogos_jogo j
LEFT JOIN jogos_avaliacao a ON a.jogo_id = j.id
GROUP BY j.id, j.nome
ORDER BY avaliacoes DESC;

SELECT p.nome AS plataforma, COUNT(jp.jogo_id) AS jogos
FROM jogos_plataforma p
LEFT JOIN jogos_jogo_plataformas jp ON jp.plataforma_id = p.id
GROUP BY p.id, p.nome
ORDER BY jogos DESC;
