CREATE PROCEDURE IF NOT EXISTS get_visible_posts(
    IN viewer_id INT,
    IN target_user_id INT
)
BEGIN
    SELECT p.*, 
           CASE WHEN l.user_id IS NOT NULL THEN 1 ELSE 0 END AS liked,
           CASE WHEN p.user_id = viewer_id THEN 1 ELSE 0 END AS owned,
           MAX(CASE WHEN f1.follower_id = viewer_id THEN 1 ELSE 0 END) AS `following`,
           MAX(CASE WHEN f2.followee_id = viewer_id THEN 1 ELSE 0 END) AS `followed`
    FROM posts_view p
    LEFT JOIN follows f1 ON p.user_id = f1.followee_id
    LEFT JOIN follows f2 ON p.user_id = f2.follower_id
    LEFT JOIN likes l ON p.post_id = l.post_id AND l.user_id = viewer_id
    WHERE (target_user_id IS NULL OR p.user_id = target_user_id) AND (
        p.privacy = 'public' OR p.user_id = viewer_id
        OR (p.privacy = 'friends' AND f1.follower_id = viewer_id AND f2.followee_id = viewer_id))
    GROUP BY p.post_id
    ORDER BY p.created_at DESC;
END;


CREATE PROCEDURE IF NOT EXISTS get_post(
    IN viewer_id INT,
    IN post_id INT
)
BEGIN
    SELECT p.*, 
           CASE WHEN l.user_id IS NOT NULL THEN 1 ELSE 0 END AS liked,
           CASE WHEN p.user_id = viewer_id THEN 1 ELSE 0 END AS owned,
           MAX(CASE WHEN f1.follower_id = viewer_id THEN 1 ELSE 0 END) AS `following`,
           MAX(CASE WHEN f2.followee_id = viewer_id THEN 1 ELSE 0 END) AS `followed`
    FROM posts_view p
    LEFT JOIN follows f1 ON p.user_id = f1.followee_id
    LEFT JOIN follows f2 ON p.user_id = f2.follower_id
    LEFT JOIN likes l ON p.post_id = l.post_id AND l.user_id = viewer_id
    WHERE p.post_id = post_id AND (
        p.privacy = 'public' OR p.user_id = viewer_id
        OR (p.privacy = 'friends' AND f1.follower_id = viewer_id AND f2.followee_id = viewer_id))
    GROUP BY p.post_id
    LIMIT 1;
END;


CREATE PROCEDURE IF NOT EXISTS get_profile(
    IN viewer_id INT,
    IN target_user_id INT
)
BEGIN
    SELECT u.*,
           MAX(CASE WHEN f1.follower_id = viewer_id THEN 1 ELSE 0 END) AS `following`,
           MAX(CASE WHEN f2.followee_id = viewer_id THEN 1 ELSE 0 END) AS `followed`
    FROM users_view u
    LEFT JOIN follows f1 ON u.user_id = f1.followee_id
    LEFT JOIN follows f2 ON u.user_id = f2.follower_id
    WHERE u.user_id = target_user_id
    GROUP BY u.user_id
    LIMIT 1;
END;
    