-- 动态视图
CREATE VIEW IF NOT EXISTS posts_view AS
SELECT p.*,
       COUNT(DISTINCT l.like_id) AS like_count,
       COUNT(DISTINCT c.comment_id) AS comment_count
FROM posts p
LEFT JOIN likes l ON p.post_id = l.post_id
LEFT JOIN comments c ON p.post_id = c.post_id
GROUP BY p.post_id;
