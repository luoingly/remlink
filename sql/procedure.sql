CREATE PROCEDURE IF NOT EXISTS get_visible_posts(
    IN viewer_id INT,
    IN target_user_id INT,
    IN `offset` INT,
    IN `limit` INT
)
BEGIN
    SELECT DISTINCT p.*, 
           CASE WHEN l.user_id IS NOT NULL THEN 1 ELSE 0 END AS liked
    FROM posts_view p
    LEFT JOIN follows f1 ON p.user_id = f1.followee_id
    LEFT JOIN follows f2 ON p.user_id = f2.follower_id
    LEFT JOIN likes l ON p.post_id = l.post_id AND l.user_id = viewer_id
    WHERE (target_user_id IS NULL OR p.user_id = target_user_id) AND (
        p.privacy = 'public' OR p.user_id = viewer_id
        OR (p.privacy = 'friends' AND f1.follower_id = viewer_id AND f2.followee_id = viewer_id))
    ORDER BY p.created_at DESC
    LIMIT `offset`, `limit`;
END;


CREATE PROCEDURE IF NOT EXISTS get_post(
    IN viewer_id INT,
    IN post_id INT
)
BEGIN
    SELECT p.*, 
           CASE WHEN l.user_id IS NOT NULL THEN 1 ELSE 0 END AS liked
    FROM posts_view p
    LEFT JOIN follows f1 ON p.user_id = f1.followee_id
    LEFT JOIN follows f2 ON p.user_id = f2.follower_id
    LEFT JOIN likes l ON p.post_id = l.post_id AND l.user_id = viewer_id
    WHERE p.post_id = post_id AND (
        p.privacy = 'public' OR p.user_id = viewer_id
        OR (p.privacy = 'friends' AND f1.follower_id = viewer_id AND f2.followee_id = viewer_id))
    LIMIT 1;
END;
