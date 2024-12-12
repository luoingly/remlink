-- 动态视图
CREATE VIEW IF NOT EXISTS posts_view AS
SELECT p.*,
       COUNT(DISTINCT l.like_id) AS like_count,
       COUNT(DISTINCT c.comment_id) AS comment_count
FROM posts p
LEFT JOIN likes l ON p.post_id = l.post_id
LEFT JOIN comments c ON p.post_id = c.post_id
GROUP BY p.post_id;

-- 用户资料视图
CREATE VIEW IF NOT EXISTS users_view AS
SELECT u.*,
       COUNT(DISTINCT f.follow_id) AS follower_count,
       COUNT(DISTINCT f2.follow_id) AS followee_count
FROM users u
LEFT JOIN follows f ON u.user_id = f.followee_id
LEFT JOIN follows f2 ON u.user_id = f2.follower_id
GROUP BY u.user_id;
