from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WeatherBase(BaseModel):
    """天气数据基础模式"""
    city: str
    country: str
    temperature: float
    humidity: int
    wind_speed: float
    description: str
    icon: str


class WeatherCreate(WeatherBase):
    """创建天气数据的模式"""
    pass


class WeatherUpdate(BaseModel):
    """更新天气数据的模式"""
    temperature: Optional[float] = None
    humidity: Optional[int] = None
    wind_speed: Optional[float] = None
    description: Optional[str] = None
    icon: Optional[str] = None


class WeatherInDB(WeatherBase):
    """数据库中天气数据的模式"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class WeatherResponse(WeatherBase):
    """API响应的天气数据模式"""
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class ForecastDay(BaseModel):
    """天气预报的单日数据模式"""
    date: str
    temperature_min: float
    temperature_max: float
    humidity: int
    wind_speed: float
    description: str
    icon: str


class WeatherForecast(BaseModel):
    """天气预报数据模式"""
    city: str
    country: str
    forecast: list[ForecastDay]
