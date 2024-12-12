# Remlink

一个定位为数据库课程设计的迷你社交平台。

## 安装与使用

### 下载 MDUI 静态文件

```bash
python install.py
```

### 运行服务端

```bash
python main.py
```

## 数据库表结构

### 用户表 (`users`)

| 字段名       | 数据类型    | 约束条件                    | 说明                   |
| ------------ | ----------- | --------------------------- | ---------------------- |
| `user_id`    | INT         | AUTO_INCREMENT, PRIMARY KEY | 用户唯一标识符         |
| `username`   | VARCHAR(20) | UNIQUE, NOT NULL            | 用户名，唯一且不能为空 |
| `password`   | CHAR(60)    | NOT NULL                    | 用户密码，使用哈希存储 |
| `created_at` | DATETIME    | DEFAULT CURRENT_TIMESTAMP   | 用户注册时间           |
| `bio`        | TEXT        |                             | 用户个人简介           |

### 用户关注表 (`follows`)

| 字段名        | 数据类型 | 约束条件                              | 说明               |
| ------------- | -------- | ------------------------------------- | ------------------ |
| `follow_id`   | INT      | AUTO_INCREMENT, PRIMARY KEY           | 关注记录唯一标识符 |
| `follower_id` | INT      | NOT NULL, FOREIGN KEY (users.user_id) | 关注者用户 ID      |
| `followee_id` | INT      | NOT NULL, FOREIGN KEY (users.user_id) | 被关注者用户 ID    |
| `created_at`  | DATETIME | DEFAULT CURRENT_TIMESTAMP             | 关注时间           |

### 动态表 (`posts`)

| 字段名       | 数据类型                             | 约束条件                              | 说明           |
| ------------ | ------------------------------------ | ------------------------------------- | -------------- |
| `post_id`    | INT                                  | AUTO_INCREMENT, PRIMARY KEY           | 动态唯一标识符 |
| `user_id`    | INT                                  | NOT NULL, FOREIGN KEY (users.user_id) | 发布者用户 ID  |
| `content`    | TEXT                                 | NOT NULL                              | 动态内容       |
| `created_at` | DATETIME                             | DEFAULT CURRENT_TIMESTAMP             | 动态发布时间   |
| `privacy`    | ENUM('public', 'friends', 'private') | DEFAULT 'public'                      | 动态可见性     |

### 点赞表 (`likes`)

| 字段名       | 数据类型 | 约束条件                              | 说明               |
| ------------ | -------- | ------------------------------------- | ------------------ |
| `like_id`    | INT      | AUTO_INCREMENT, PRIMARY KEY           | 点赞记录唯一标识符 |
| `user_id`    | INT      | NOT NULL, FOREIGN KEY (users.user_id) | 点赞者用户 ID      |
| `post_id`    | INT      | NOT NULL, FOREIGN KEY (posts.post_id) | 被点赞的动态 ID    |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP             | 点赞时间           |

### 评论表 (`comments`)

| 字段名       | 数据类型 | 约束条件                              | 说明            |
| ------------ | -------- | ------------------------------------- | --------------- |
| `comment_id` | INT      | AUTO_INCREMENT, PRIMARY KEY           | 评论唯一标识符  |
| `user_id`    | INT      | NOT NULL, FOREIGN KEY (users.user_id) | 评论者用户 ID   |
| `post_id`    | INT      | NOT NULL, FOREIGN KEY (posts.post_id) | 被评论的动态 ID |
| `content`    | TEXT     | NOT NULL                              | 评论内容        |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP             | 评论时间        |
