# Stellar Weather API 文档

## 概述

Stellar Weather API 提供星象与天气的趣味数据服务，支持实时天气查询、星象运势查询以及结合两者的趣味分析。

## 基本信息

- API 基础 URL: `http://localhost:8000`
- 文档地址: `http://localhost:8000/docs` (Swagger UI)
- 文档地址: `http://localhost:8000/redoc` (ReDoc)

## 认证

目前 API 无需认证即可访问，生产环境建议添加 API 密钥或 OAuth2 认证。

## 响应格式

所有 API 响应均采用 JSON 格式，包含以下字段：

```json
{
  "success": true,
  "data": { ... },
  "message": "操作成功"
}
```

错误响应格式：

```json
{
  "success": false,
  "detail": "错误信息",
  "code": 404
}
```

## 状态码

- `200` - 请求成功
- `400` - 错误的请求参数
- `404` - 资源未找到
- `500` - 服务器内部错误
- `503` - 服务不可用（如外部 API 调用失败）

## 健康检查接口

### 获取欢迎信息

**请求**:
```
GET /
```

**响应**:
```json
{
  "message": "Welcome to Stellar Weather API!",
  "version": "1.0.0"
}
```

### 健康检查

**请求**:
```
GET /health
```

**响应**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "service": "stellar-weather-api"
}
```

## 天气相关接口

### 获取城市当前天气

**请求**:
```
GET /api/weather/{city}
```

**参数**:
- `city` (路径参数): 城市名称（如：北京、上海、New York）

**响应**:
```json
{
  "id": 1,
  "city": "北京",
  "country": "CN",
  "temperature": 25.5,
  "humidity": 60,
  "wind_speed": 3.5,
  "description": "晴",
  "icon": "01d",
  "last_updated": "2024-01-01T12:00:00Z"
}
```

### 获取城市天气预报

**请求**:
```
GET /api/weather/forecast/{city}?days=5
```

**参数**:
- `city` (路径参数): 城市名称
- `days` (查询参数): 预报天数（默认：5，最大：7）

**响应**:
```json
{
  "city": "北京",
  "country": "CN",
  "forecast": [
    {
      "date": "2024-01-01",
      "temperature_min": 20.0,
      "temperature_max": 28.0,
      "humidity": 55,
      "wind_speed": 3.0,
      "description": "晴",
      "icon": "01d"
    },
    // 更多预报数据...
  ]
}
```

### 获取城市天气历史数据

**请求**:
```
GET /api/weather/history/{city}?limit=10
```

**参数**:
- `city` (路径参数): 城市名称
- `limit` (查询参数): 返回记录数量（默认：10，最大：100）

**响应**:
```json
{
  "city": "北京",
  "history": [
    {
      "id": 1,
      "temperature": 25.5,
      "humidity": 60,
      "wind_speed": 3.5,
      "description": "晴",
      "icon": "01d",
      "recorded_at": "2024-01-01T12:00:00Z"
    },
    // 更多历史数据...
  ]
}
```

## 星象相关接口

### 获取星座完整运势

**请求**:
```
GET /api/horoscope/{sign}
```

**参数**:
- `sign` (路径参数): 星座名称（如：白羊座、金牛座、Gemini）

**响应**:
```json
{
  "id": 1,
  "sign": "白羊座",
  "date_range": "3月21日-4月19日",
  "today": "白羊座今日运势：整体运势良好，工作顺利，感情稳定。",
  "tomorrow": "白羊座明日运势：运势一般，需要注意人际关系。",
  "week": "白羊座本周运势：本周整体运势上升，适合开展新项目。",
  "month": "白羊座本月运势：本月运势平稳，财运不错。",
  "year": "白羊座本年运势：本年运势起伏较大，需要注意健康。",
  "last_updated": "2024-01-01T00:00:00Z"
}
```

### 获取星座今日运势

**请求**:
```
GET /api/horoscope/{sign}/today
```

**参数**:
- `sign` (路径参数): 星座名称

**响应**:
```json
{
  "sign": "白羊座",
  "date_range": "3月21日-4月19日",
  "today": "白羊座今日运势：整体运势良好，工作顺利，感情稳定。",
  "last_updated": "2024-01-01T00:00:00Z"
}
```

### 获取所有星座今日运势

**请求**:
```
GET /api/horoscope/all/today
```

**响应**:
```json
[
  {
    "sign": "白羊座",
    "date_range": "3月21日-4月19日",
    "today": "白羊座今日运势：整体运势良好..."
  },
  {
    "sign": "金牛座",
    "date_range": "4月20日-5月20日",
    "today": "金牛座今日运势：财运不错..."
  },
  // 其他星座数据...
]
```

## 趣味分析接口

### 获取天气与星座分析

**请求**:
```
GET /api/analysis?city={city}&sign={sign}
```

**参数**:
- `city` (查询参数): 城市名称
- `sign` (查询参数): 星座名称

**响应**:
```json
{
  "city": "北京",
  "weather": {
    "temperature": 25.5,
    "description": "晴"
  },
  "sign": "白羊座",
  "horoscope": {
    "today": "白羊座今日运势：整体运势良好..."
  },
  "analysis": "白羊座今日运势良好，北京天气晴朗，适合户外活动和社交聚会。建议利用良好的天气和运势，开展新的工作计划或约会安排。"
}
```

## 外部 API 依赖

- [OpenWeatherMap API](https://openweathermap.org/api): 提供天气数据
- [Horoscope API](https://example.com/horoscope-api): 提供星象数据（模拟）

## 数据缓存策略

- 天气数据缓存 1 小时
- 星象数据缓存 1 天
- 使用数据库存储历史数据

## 限制

- 每分钟最多 60 个请求
- 每次获取预报最多 7 天
- 每次获取历史数据最多 100 条

## 常见问题

### Q: 为什么返回的天气数据不是最新的？
A: 天气数据会缓存 1 小时，1 小时内重复请求会返回缓存数据。

### Q: 支持哪些城市？
A: 支持全球主要城市，使用城市名称或城市 ID 均可。

### Q: 支持哪些星座？
A: 支持 12 个传统星座：白羊座、金牛座、双子座、巨蟹座、狮子座、处女座、天秤座、天蝎座、射手座、摩羯座、水瓶座、双鱼座。

## 版本历史

### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持天气查询和星象查询
- 提供趣味分析功能

## 联系方式

- 项目维护者: [Your Name]
- 邮箱: [your.email@example.com]
- GitHub: [yourusername](https://github.com/yourusername)
