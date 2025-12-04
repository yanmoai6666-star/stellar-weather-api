# Stellar Weather API

一个提供星象与天气趣味数据服务的API后端项目。

## 功能特性

- 提供实时天气数据查询
- 提供星象数据查询
- 结合天气和星象的趣味分析
- RESTful API设计
- 支持多种数据格式输出

## 技术栈

- Python 3.11
- FastAPI 框架
- PostgreSQL 数据库
- SQLAlchemy ORM
- Pydantic 数据验证

## 快速开始

### 环境要求

- Python 3.11+
- PostgreSQL 14+ 或 SQLite 3.9+
- Git

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/stellar-weather-api.git
cd stellar-weather-api
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 开发依赖
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，配置数据库连接等信息
```

5. 数据库初始化
```bash
# 开发环境会自动创建SQLite数据库
# 如果使用PostgreSQL，请先创建数据库
python -c "from app.utils.database import Base, engine; Base.metadata.create_all(bind=engine)"

6. 启动开发服务器
```bash
uvicorn app.main:app --reload
```

7. 访问API文档
```
http://localhost:8000/docs
```

## API 端点

### 健康检查
- `GET /` - 欢迎页面
- `GET /health` - 健康检查接口

### 天气相关
- `GET /api/weather/{city}` - 获取城市当前天气
- `GET /api/weather/forecast/{city}` - 获取城市天气预报
- `GET /api/weather/history/{city}` - 获取城市天气历史数据

### 星象相关
- `GET /api/horoscope/{sign}` - 获取星座完整运势
- `GET /api/horoscope/{sign}/today` - 获取星座今日运势
- `GET /api/horoscope/all/today` - 获取所有星座今日运势

### 趣味分析
- `GET /api/analysis?city={city}&sign={sign}` - 获取城市天气与星座的趣味分析

## 项目结构

```
stellar-weather-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # 应用入口
│   ├── api/
│   │   ├── __init__.py
│   │   ├── weather.py       # 天气API路由
│   │   ├── horoscope.py     # 星象API路由
│   │   └── analysis.py      # 分析API路由
│   ├── models/
│   │   ├── __init__.py
│   │   ├── weather.py       # 天气数据模型
│   │   └── horoscope.py     # 星象数据模型
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── weather.py       # 天气数据模式
│   │   └── horoscope.py     # 星象数据模式
│   ├── services/
│   │   ├── __init__.py
│   │   ├── weather_service.py  # 天气服务层
│   │   └── horoscope_service.py # 星象服务层
│   └── utils/
│       ├── __init__.py
│       ├── database.py      # 数据库配置
│       └── settings.py      # 应用配置
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # 测试配置
│   ├── test_weather.py      # 天气API测试
│   ├── test_horoscope.py    # 星象API测试
│   ├── test_analysis.py     # 分析API测试
│   └── test_services.py     # 服务层测试
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # CI/CD工作流配置
├── .env                     # 环境变量（开发环境）
├── .env.example             # 环境变量示例
├── .gitignore
├── Dockerfile               # Docker构建文件
├── docker-compose.yml       # Docker Compose配置
├── README.md
├── requirements.txt         # 生产依赖
├── requirements-dev.txt     # 开发依赖
└── pyproject.toml           # 项目元数据
```

## 测试

运行测试套件：

```bash
pytest tests/ -v --cov=app/
```

## 部署

### Docker 部署

```bash
docker-compose up -d
```

### 生产环境部署

建议使用 Gunicorn + Nginx 部署：

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## 贡献指南

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

- 项目维护者: [Your Name]
- 邮箱: [your.email@example.com]
- GitHub: [yourusername](https://github.com/yourusername)
