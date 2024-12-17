-- 用户资料视图
CREATE VIEW IF NOT EXISTS users_view AS
SELECT u.user_id, u.username, u.bio,
       COUNT(DISTINCT f1.follow_id) AS follower_count,
       COUNT(DISTINCT f2.follow_id) AS followee_count
FROM users u
LEFT JOIN follows f1 ON u.user_id = f1.followee_id
LEFT JOIN follows f2 ON u.user_id = f2.follower_id
GROUP BY u.user_id;


-- 动态视图
CREATE VIEW IF NOT EXISTS posts_view AS
SELECT p.*, u.username, u.bio, u.follower_count, u.followee_count,
    (SELECT COUNT(like_id) 
        FROM likes l WHERE l.post_id = p.post_id) AS like_count
FROM posts p
LEFT JOIN users_view u ON p.user_id = u.user_id;
