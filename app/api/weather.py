from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.utils.database import get_db
from app.schemas.weather import WeatherResponse, WeatherForecast
from app.services.weather_service import WeatherService

# 创建路由实例
router = APIRouter()


@router.get("/{city}", response_model=WeatherResponse, summary="获取城市天气")
async def get_weather(
    city: str,
    db: Session = Depends(get_db)
):
    """根据城市名称获取实时天气数据"""
    weather_service = WeatherService(db)
    
    # 尝试获取天气数据
    weather = weather_service.get_or_fetch_weather(city)
    
    if not weather:
        raise HTTPException(status_code=404, detail=f"未找到城市 {city} 的天气数据")
    
    return weather


@router.get("/forecast/{city}", response_model=WeatherForecast, summary="获取天气预报")
async def get_weather_forecast(
    city: str,
    days: int = Query(7, ge=1, le=14, description="预报天数，1-14天"),
    db: Session = Depends(get_db)
):
    """根据城市名称获取天气预报数据"""
    weather_service = WeatherService(db)
    
    # 从API获取天气预报数据
    api_data = weather_service.fetch_forecast_from_api(city)
    
    if not api_data:
        raise HTTPException(status_code=404, detail=f"未找到城市 {city} 的天气预报数据")
    
    # 解析API响应
    forecast = weather_service.parse_forecast_api_response(api_data)
    
    # 限制预报天数
    forecast.forecast = forecast.forecast[:days]
    
    return forecast


@router.get("/history/{city}", response_model=list[WeatherResponse], summary="获取天气历史数据")
async def get_weather_history(
    city: str,
    limit: int = Query(10, ge=1, le=100, description="返回记录数，1-100条"),
    db: Session = Depends(get_db)
):
    """根据城市名称获取天气历史数据"""
    from app.models.weather import Weather
    
    # 从数据库获取历史数据
    history = db.query(Weather).filter(
        Weather.city == city
    ).order_by(Weather.created_at.desc()).limit(limit).all()
    
    if not history:
        raise HTTPException(status_code=404, detail=f"未找到城市 {city} 的天气历史数据")
    
    return history
