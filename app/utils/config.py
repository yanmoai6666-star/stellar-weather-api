from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """应用配置类，用于加载环境变量"""
    
    # 应用基本配置
    APP_NAME: str = "Stellar Weather API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str
    
    # API配置
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["*"]
    
    # 外部API配置
    WEATHER_API_KEY: str = ""
    HOROSCOPE_API_KEY: str = ""
    
    # 日志配置
    LOG_LEVEL: str = "INFO"

    WEATHER_CACHE_TTL_MINUTES: int = 60  # 天气缓存默认60分钟
    HOROSCOPE_CACHE_TTL_DAYS: int = 1    # 星象缓存默认1天

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# 创建配置实例
settings = Settings()
