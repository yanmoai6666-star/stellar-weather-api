# Stellar Weather API 部署指南

## 环境要求

### 开发环境
- Python 3.11+
- SQLite 3.9+ (默认)
- Git

### 生产环境
- Python 3.11+
- PostgreSQL 14+
- Redis (可选，用于缓存)
- Nginx 或 Apache (用于反向代理)
- Docker (可选，用于容器化部署)

## 部署方式

### 1. 传统部署方式

#### 1.1 安装依赖

```bash
# 克隆仓库
git clone https://github.com/yourusername/stellar-weather-api.git
cd stellar-weather-api

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

#### 1.2 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑环境变量文件
vim .env  # 或使用其他编辑器
```

主要配置项：

- `APP_ENV`: 设置为 `production`
- `DATABASE_URL`: PostgreSQL 数据库连接字符串
- `OPENWEATHERMAP_API_KEY`: OpenWeatherMap API 密钥
- `HOROSCOPE_API_KEY`: 星象 API 密钥
- `SECRET_KEY`: 用于安全功能的密钥

#### 1.3 初始化数据库

```bash
# 创建数据库表
python -c "from app.utils.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

#### 1.4 启动应用

```bash
# 使用 Gunicorn 启动生产服务器
pip install gunicorn

gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

### 2. Docker 部署方式

#### 2.1 安装 Docker

请参考 [Docker 官方文档](https://docs.docker.com/get-docker/) 安装 Docker 和 Docker Compose。

#### 2.2 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑环境变量文件
vim .env  # 或使用其他编辑器
```

#### 2.3 启动容器

```bash
# 使用 Docker Compose 启动所有服务
docker-compose up -d
```

这将启动以下服务：
- `stellar-weather-api`: 主应用容器
- `stellar-weather-db`: PostgreSQL 数据库容器
- `stellar-weather-pgadmin`: pgAdmin 管理界面 (可选)

#### 2.4 访问应用

应用将在 `http://localhost:8000` 上运行。

#### 2.5 管理容器

```bash
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart
```

### 3. 使用 Nginx 作为反向代理

#### 3.1 安装 Nginx

```bash
# Ubuntu/Debian
apt-get update && apt-get install nginx

# CentOS/RHEL
yum install nginx
```

#### 3.2 配置 Nginx

创建 Nginx 配置文件：

```bash
vim /etc/nginx/conf.d/stellar-weather-api.conf
```

添加以下内容：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /docs {
        proxy_pass http://localhost:8000/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /redoc {
        proxy_pass http://localhost:8000/redoc;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 3.3 测试并重启 Nginx

```bash
# 测试配置
nginx -t

# 重启 Nginx
systemctl restart nginx
```

### 4. 使用 Systemd 管理服务

#### 4.1 创建 Systemd 服务文件

```bash
vim /etc/systemd/system/stellar-weather-api.service
```

添加以下内容：

```ini
[Unit]
Description=Stellar Weather API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/stellar-weather-api
Environment="PATH=/path/to/stellar-weather-api/venv/bin"
ExecStart=/path/to/stellar-weather-api/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 4.2 启动并启用服务

```bash
# 重新加载 Systemd 配置
systemctl daemon-reload

# 启动服务
systemctl start stellar-weather-api

# 设置开机自启
systemctl enable stellar-weather-api

# 查看服务状态
systemctl status stellar-weather-api
```

## 监控与维护

### 日志

- 应用日志：`logs/app.log`
- Nginx 日志：`/var/log/nginx/access.log` 和 `/var/log/nginx/error.log`
- Systemd 日志：`journalctl -u stellar-weather-api`

### 数据库备份

```bash
# 备份 PostgreSQL 数据库
pg_dump -U postgres stellar_weather_db > backup_$(date +%Y%m%d_%H%M%S).sql

# 恢复数据库
psql -U postgres stellar_weather_db < backup.sql
```

### 性能优化

1. **增加 Gunicorn 工作进程数**：
   ```bash
   gunicorn -w 8 -k uvicorn.workers.UvicornWorker app.main:app
   ```
   建议工作进程数为 CPU 核心数的 2-4 倍。

2. **启用 Redis 缓存**：
   - 安装 Redis
   - 修改配置文件使用 Redis 作为缓存后端

3. **启用数据库连接池**：
   - 配置 SQLAlchemy 使用连接池
   - 在生产环境中调整连接池大小

4. **使用 CDN 加速静态资源**：
   - 对于 Swagger UI 和 ReDoc 等静态资源，考虑使用 CDN

## 安全建议

1. **使用 HTTPS**：
   - 安装 SSL 证书（推荐使用 Let's Encrypt）
   - 配置 Nginx 支持 HTTPS

2. **限制访问**：
   - 使用防火墙限制访问端口
   - 配置 Nginx 访问控制

3. **保护敏感信息**：
   - 不在代码中硬编码 API 密钥和密码
   - 使用环境变量管理敏感信息
   - 定期更换 API 密钥和密码

4. **更新依赖**：
   - 定期更新依赖包以修复安全漏洞
   - 使用 `pip-audit` 或类似工具检查依赖安全性

5. **启用日志监控**：
   - 配置日志监控工具（如 ELK Stack、Prometheus + Grafana）
   - 设置异常告警

## 常见问题

### Q: 应用无法启动
A: 检查以下几点：
- 环境变量是否正确配置
- 数据库连接是否正常
- 端口是否被占用
- 查看应用日志获取详细错误信息

### Q: 为什么返回 503 错误
A: 通常是由于外部 API 调用失败导致的：
- 检查 API 密钥是否有效
- 检查网络连接
- 查看应用日志中的外部 API 调用情况

### Q: 如何升级应用版本
A: 
1. 停止服务
2. 拉取最新代码
3. 更新依赖
4. 应用数据库迁移（如果有）
5. 启动服务

## 联系方式

- 项目维护者: [Your Name]
- 邮箱: [your.email@example.com]
- GitHub: [yourusername](https://github.com/yourusername)
