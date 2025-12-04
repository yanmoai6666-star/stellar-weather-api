from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import weather, horoscope, analysis
from app.utils.config import settings

# 创建FastAPI应用实例
app = FastAPI(
    title="Stellar Weather API",
    description="一个提供星象与天气趣味数据服务的API后端项目",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(weather.router, prefix="/api/weather", tags=["weather"])
app.include_router(horoscope.router, prefix="/api/horoscope", tags=["horoscope"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])


@app.get("/")
async def root():
    """根路径，返回API基本信息"""
    return {
        "message": "Welcome to Stellar Weather API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}
