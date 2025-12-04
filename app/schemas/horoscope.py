from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HoroscopeBase(BaseModel):
    """星象数据基础模式"""
    sign: str
    date_range: str
    today: str
    tomorrow: str
    week: str
    month: str
    year: str


class HoroscopeCreate(HoroscopeBase):
    """创建星象数据的模式"""
    pass


class HoroscopeUpdate(BaseModel):
    """更新星象数据的模式"""
    today: Optional[str] = None
    tomorrow: Optional[str] = None
    week: Optional[str] = None
    month: Optional[str] = None
    year: Optional[str] = None


class HoroscopeInDB(HoroscopeBase):
    """数据库中星象数据的模式"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class HoroscopeResponse(BaseModel):
    """API响应的星象数据模式"""
    sign: str
    date_range: str
    today: str
    tomorrow: str
    week: str
    month: str
    year: str
    
    class Config:
        orm_mode = True


class TodayHoroscope(BaseModel):
    """今日运势数据模式"""
    sign: str
    date_range: str
    today: str
    
    class Config:
        orm_mode = True
