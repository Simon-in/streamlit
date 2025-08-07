# 简单的演示SQL文件 - 可以用于测试格式化和语法检查功能

# 1. 简单的SELECT语句
SELECT id, username, email
FROM users
WHERE status = 'active'
ORDER BY created_at DESC
LIMIT 10;

# 2. 带有JOIN的复杂SELECT语句
SELECT 
    u.id,
    u.username,
    p.profile_name,
    COUNT(o.id) as order_count
FROM 
    users u
LEFT JOIN 
    profiles p ON u.id = p.user_id
LEFT JOIN 
    orders o ON u.id = o.user_id
WHERE 
    u.created_at > '2023-01-01'
GROUP BY 
    u.id, u.username, p.profile_name
HAVING 
    COUNT(o.id) > 5
ORDER BY 
    order_count DESC
LIMIT 20;

# 3. INSERT语句
INSERT INTO products (name, category, price, stock)
VALUES ('New Product', 'Electronics', 499.99, 100);

# 4. UPDATE语句
UPDATE users
SET 
    status = 'inactive',
    last_updated = CURRENT_TIMESTAMP
WHERE last_login < DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR);

# 5. 创建表语句
CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive', 'banned') DEFAULT 'active'
);
