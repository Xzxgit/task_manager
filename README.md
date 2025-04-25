# Task Manager API
# 任务管理系统 API

## 安装

1. 克隆仓库
2. 创建虚拟环境：
   ```bash
   手动在PyCharm创建venv虚拟环境, 
   或 执行以下命令
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
3. ```bash
   cd 项目根目录
   pip install -r requirements.txt
   # 配置完数据库在执行这一步
   uvicorn app.main:app --reload
4. 数据库配置
   ```sql
   -- 创建数据库
   CREATE DATABASE task_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

   -- 使用数据库
   USE task_db;

   -- 创建任务表
   CREATE TABLE tasks (
       id INT AUTO_INCREMENT PRIMARY KEY,
       title VARCHAR(100) NOT NULL,
       description VARCHAR(500),
       due_date DATETIME,
       priority INT DEFAULT 2,
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
       updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
   );

   -- 添加索引（可选，用于优化查询性能）
   CREATE INDEX idx_priority ON tasks(priority);
   CREATE INDEX idx_due_date ON tasks(due_date);
   
   若要创建新用户
   CREATE USER 'task_user'@'localhost' IDENTIFIED BY 'password';
   GRANT ALL PRIVILEGES ON task_db.* TO 'task_user'@'localhost';
   FLUSH PRIVILEGES;
   
   -- 在database.py文件下换成自己的数据库账号密码
   
5. 接口文档
   ```bash
   项目在本地跑起来可以通过浏览器访问 
   127.0.0.1:8000/docs 查看
6. 单元测试
   ```bash
   首先在 database.py 
   注释掉开发数据库, 打开测试数据库. 然后执行以下步骤
   cd 项目根目录
   python -m pytest --cov=app 或 python -m pytest --cov=app --cov-report=html
   后者可以通过查看新生成目录下的 index.html 查看详细的测试报告
   
